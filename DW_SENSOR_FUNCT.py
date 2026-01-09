#------------------------------------------------------------------------------------------------#
#-------------------------------------- DUCKWEED LABS -------------------------------------------#
# Last Update Name: Owen Sowalla
# Last Update Date: 01/04/2026
#
# This program file serves as a first prototype of what will be the central program file for the
# Duckweed Labs team to use for the DPSD prototype slated for completion in January of 2026. It
# includes setup, running, and output without worrying about visuals (to be done in a second
# iteration). Future updates include honing in on i2c fixes, display, and file/data logging.
#
# For reader reference:
#
# - dht22 = Temp/Humidity Sensor
# - mhz19 = CO2 Sensor
# - AS7343 = Spectral Sensor
# - mlx90640 = Thermal Sensor
#
#------------------------------------------------------------------------------------------------#

# Library Imports

import time
import board
import adafruit_dht
import os
os.environ["BLINKA_MLX90640_FORCE_BLOCK"]= "16"
import numpy as np
import matplotlib.pyplot as plt
import busio
import adafruit_mlx90640
import serial
import qwiic_as7343
import sys

# Global Initialization

# # dht22
dht = None

# # mhz19
#READ_INTERVAL_SECONDS = 0
SERIAL_PORT_NAME = ""
SERIAL_PORT_BAUD_RATE = 0
ser = None
cmd = None

# # as7343
myAS7343 = None
file = None

# # mlx90640
i2c = None
mlx = None
frame = 0
fig = None
ax = None
img = None

# Setup Functions

def sens_dht22_setup():
    global dht
    dht = adafruit_dht.DHT22(board.D4)
    print("\nTest 1: dht22 : Complete\n")
    return

def sens_mhz19_setup():
    global READ_INTERVAL_SECONDS, SERIAL_PORT_NAME, SERIAL_PORT_BAUD_RATE, ser, cmd
    #READ_INTERVAL_SECONDS = 0.5
    SERIAL_PORT_NAME = "/dev/ttyAMA0"
    SERIAL_PORT_BAUD_RATE = 9600

    ser = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUD_RATE, timeout=1)
    cmd = bytearray ([0xFF, 0X01, 0X86, 0 ,0, 0, 0, 0, 0X79])
    print("\nTest 2: mhz19 : Complete\n")
    return

def sens_spect_setup():
    global myAS7343, file
    myAS7343 = qwiic_as7343.QwiicAS7343()

    if myAS7343.is_connected() == False:
            print("The device isn't connected to the system. Please check your connection", \
                    file=sys.stderr)
            return

    if not myAS7343.begin():
            print("The device isn't connected to the system. Please check your connection", \
                    file=sys.stderr)
            return

    myAS7343.power_on()
    print("Device powered on")

    if not myAS7343.set_auto_smux(myAS7343.kAutoSmux18Channels):
            print("Failed to set AutoSmux", file=sys.stderr)
            return
    print("AutoSmux set to 18 channels")

    if not myAS7343.spectral_measurement_enable():
            print("Failed to enable spectral measurements", file=sys.stderr)
            return
    print("Spectral measurements enabled")
    print("\nTest 3: as7343 : Completed\n")
    return

def sens_therm_setup():
    global i2c, mlx, frame, fig, ax, img
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    print("\nTest 4: mlx90640 : Completed\n")
    return

# Reading Functions

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
            print ("CO2:", co2, "ppm")
            print ("Response length (bytes):", len(resp))
            print ("Raw response:", resp)
            print ("")
            return co2
    else:
            print("invalid response:", resp)
            return -1
    #time.sleep(READ_INTERVAL_SECONDS)
    return

def sens_spect_read():
    myAS7343.set_led_drive(0) # 0 = 4mA
    myAS7343.set_led_on()

    time.sleep(0.100) # Wait 100 ms for LED to fully illuminate our target

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


#    print(myAS7343.get_blue(), end=',')
#    print(myAS7343.get_red(), end=',')
#    print(myAS7343.get_green(), end=',')
#    print(myAS7343.get_nir(), end=',\n')

    #time.sleep(0.500) # Wait 500 ms before next reading
    return red, green, blue, nir

def sens_therm_read():
    frame = [0] * 768

    plt.ion()
    fig, ax = plt.subplots(figsize=(6,4))
    img= ax.imshow(np.zeros((24,32)), cmap='inferno', vmin=20, vmax=40)
    plt.colorbar(img)

    try:
        mlx.getFrame(frame)
        print("center pixel:", frame [12*32 + 16], "C")
    except ValueError:
        print("error")
    return mlx.getFrame(frame)

# Summary Functions

def sens_setup():
    sens_dht22_setup()
    time.sleep(1)
    sens_mhz19_setup()
    time.sleep(1)
    sens_spect_setup()
    time.sleep(1)
    sens_therm_setup()
    time.sleep(1)
    print("Sensor Setup Done!")
    return

def sens_read():
    sens_dht22_read()
    time.sleep(1)
    sens_mhz19_read()
    time.sleep(1)
    sens_spect_read()
    time.sleep(1)
    sens_therm_read()
    time.sleep(1)
    print("Sensor Read Done!")
    return

'''

if __name__ == '__main__':
        try:
            print("Sensor Setup in 3...")
            time.sleep(1)
            print("2...")
            time.sleep(1)
            print("1...")
            time.sleep(1)
            sens_setup()
            time.sleep(1)
            print("Sensor Read in 3...")
            time.sleep(1)
            print("2...")
            time.sleep(1)
            print("1...")
            time.sleep(1)
            sens_read()
            sys.exit(0)
        except (KeyboardInterrupt, SystemExit) as exErr:
            print("Ending Test")
            sys.exit(0)

'''

#------------------------------------------------------------------------------------------------#
