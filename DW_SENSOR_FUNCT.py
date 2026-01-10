#------------------------------------------------------------------------------------------------#
#-------------------------------------- DUCKWEED LABS -------------------------------------------#
# Last Update Name: Owen Sowalla
# Last Update Date: 01/04/2026
#
# Sensor functions for Duckweed Labs DPSD prototype
# Includes:
# - DHT22
# - MH-Z19 CO2
# - AS7343 Spectral
# - TWO MLX90640 Thermal Cameras
#------------------------------------------------------------------------------------------------#

# -------------------- Imports --------------------

import time
import os
import sys

import board
import busio
import serial
import adafruit_dht
import adafruit_mlx90640
import qwiic_as7343

from adafruit_extended_bus import ExtendedI2C as I2C

# Force MLX90640 block mode
os.environ["BLINKA_MLX90640_FORCE_BLOCK"] = "16"

# -------------------- Globals --------------------

# DHT22
dht = None

# MH-Z19
ser = None
cmd = bytearray([0xFF, 0x01, 0x86, 0, 0, 0, 0, 0, 0x79])

# AS7343
myAS7343 = None

# Thermal cameras
i2c_hw = None
i2c_sw = None
mlx1 = None
mlx2 = None
frame1 = None
frame2 = None

# -------------------- Setup Functions --------------------

def sens_dht22_setup():
    global dht
    dht = adafruit_dht.DHT22(board.D4)
    print("\nTest 1: dht22 : Complete\n")

def sens_mhz19_setup():
    global ser
    ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
    print("\nTest 2: mhz19 : Complete\n")

def sens_spect_setup():
    global myAS7343

    myAS7343 = qwiic_as7343.QwiicAS7343()

    if not myAS7343.is_connected():
        print("AS7343 not detected", file=sys.stderr)
        return

    if not myAS7343.begin():
        print("AS7343 init failed", file=sys.stderr)
        return

    myAS7343.power_on()
    myAS7343.set_auto_smux(myAS7343.kAutoSmux18Channels)
    myAS7343.spectral_measurement_enable()

    print("\nTest 3: as7343 : Completed\n")

def sens_therm_setup():
    global i2c_hw, i2c_sw, mlx1, mlx2, frame1, frame2

    # Camera 1 — hardware I2C
    i2c_hw = busio.I2C(board.SCL, board.SDA, frequency=400000)
    mlx1 = adafruit_mlx90640.MLX90640(i2c_hw)
    mlx1.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    # Camera 2 — software I2C (/dev/i2c-3)
    i2c_sw = I2C(3)
    mlx2 = adafruit_mlx90640.MLX90640(i2c_sw)
    mlx2.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    frame1 = [0] * 768
    frame2 = [0] * 768

    print("\nTest 4 & 5: mlx90640 : Completed\n")

# -------------------- Read Functions --------------------

def sens_dht22_read():
    temperature = dht.temperature
    humidity = dht.humidity
    print(f"Temp: {temperature:.1f}*C Humidity: {humidity:.1f}%")
    return temperature, humidity

def sens_mhz19_read():
    ser.write(cmd)
    resp = ser.read(9)

    if len(resp) == 9 and resp[0] == 0xFF and resp[1] == 0x86:
        co2 = resp[2] * 256 + resp[3]
        print("CO2:", co2, "ppm")
        return co2
    else:
        print("invalid response:", resp)
        return -1

def sens_spect_read():
    myAS7343.set_led_drive(0)
    myAS7343.set_led_on()
    time.sleep(0.1)

    myAS7343.read_all_spectral_data()
    myAS7343.set_led_off()

    red = myAS7343.get_red()
    green = myAS7343.get_green()
    blue = myAS7343.get_blue()
    nir = myAS7343.get_nir()

    print(red, end=',')
    print(green, end=',')
    print(blue, end=',')
    print(nir, end=',\n')

    return red, green, blue, nir

def sens_therm_read():
    try:
        mlx1.getFrame(frame1)
        print("center pixel cam1:", frame1[12 * 32 + 16], "C")

        time.sleep(0.05)

        mlx2.getFrame(frame2)
        print("center pixel cam2:", frame2[12 * 32 + 16], "C")

        return frame1, frame2

    except ValueError:
        print("thermal read error")
        return None, None

# -------------------- Summary Functions --------------------

def sens_setup():
    print("Sensor Setup in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)

    sens_dht22_setup()
    time.sleep(1)

    sens_mhz19_setup()
    time.sleep(1)

    sens_spect_setup()
    time.sleep(1)

    sens_therm_setup()
    time.sleep(1)

    print("Sensor Setup Done!")

def sens_read():
    print("Sensor Read in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)

    sens_dht22_read()
    time.sleep(1)

    sens_mhz19_read()
    time.sleep(1)

    sens_spect_read()
    time.sleep(1)

    sens_therm_read()
    time.sleep(1)

    print("Sensor Read Done!")
