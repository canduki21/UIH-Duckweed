import os
os.environ["BLINKA_MLX90640_FORCE_BLOCK"] = "16"

import time
import board
import busio
import serial
import sys
import adafruit_dht
import adafruit_mlx90640
import qwiic_as7343
from adafruit_extended_bus import ExtendedI2C as I2C

# ================= GLOBALS =================

# DHT22
dw2_dht = None

# MH-Z19
dw2_ser = None
dw2_cmd = bytearray([0xFF,0x01,0x86,0,0,0,0,0,0x79])

# AS7343
dw2_as7343 = None

# Thermal cameras
dw2_i2c_hw = None
dw2_i2c_sw = None
dw2_mlx1 = None
dw2_mlx2 = None
dw2_frame1 = None
dw2_frame2 = None

# ================= SETUP =================

def dw2_sens_setup():
    dw2_dht_setup()
    dw2_mhz19_setup()
    dw2_spect_setup()
    dw2_therm_setup()
    print("DW2: all sensors initialized")

def dw2_dht_setup():
    global dw2_dht
    dw2_dht = adafruit_dht.DHT22(board.D4)

def dw2_mhz19_setup():
    global dw2_ser
    dw2_ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)

def dw2_spect_setup():
    global dw2_as7343
    dw2_as7343 = qwiic_as7343.QwiicAS7343()
    if not dw2_as7343.is_connected() or not dw2_as7343.begin():
        print("DW2: AS7343 not detected", file=sys.stderr)
        return
    dw2_as7343.power_on()
    dw2_as7343.set_auto_smux(dw2_as7343.kAutoSmux18Channels)
    dw2_as7343.spectral_measurement_enable()

def dw2_therm_setup():
    global dw2_i2c_hw, dw2_i2c_sw
    global dw2_mlx1, dw2_mlx2
    global dw2_frame1, dw2_frame2

    dw2_i2c_hw = busio.I2C(board.SCL, board.SDA)
    dw2_mlx1 = adafruit_mlx90640.MLX90640(dw2_i2c_hw)
    dw2_mlx1.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

    dw2_i2c_sw = I2C(3)
    dw2_mlx2 = adafruit_mlx90640.MLX90640(dw2_i2c_sw)
    dw2_mlx2.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    dw2_frame1 = [0]*768
    dw2_frame2 = [0]*768

# ================= READ =================

def dw2_sens_read():
    return {
        "dht": dw2_dht_read(),
        "co2": dw2_mhz19_read(),
        "spect": dw2_spect_read(),
        "thermal": dw2_therm_read()
    }

def dw2_dht_read():
    return dw2_dht.temperature, dw2_dht.humidity

def dw2_mhz19_read():
    dw2_ser.write(dw2_cmd)
    r = dw2_ser.read(9)
    if len(r) == 9:
        return r[2]*256 + r[3]
    return None

def dw2_spect_read():
    dw2_as7343.read_all_spectral_data()
    return [
        dw2_as7343.get_blue(),
        dw2_as7343.get_green(),
        dw2_as7343.get_red(),
        dw2_as7343.get_nir()
    ]

def dw2_therm_read():
    try:
        dw2_mlx1.getFrame(dw2_frame1)
        time.sleep(0.05)
        dw2_mlx2.getFrame(dw2_frame2)
        return dw2_frame1, dw2_frame2
    except Exception as e:
        print("DW2 thermal error:", e)
        return None, None
