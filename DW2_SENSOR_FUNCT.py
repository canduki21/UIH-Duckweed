import os
os.environ["BLINKA_MLX90640_FORCE_BLOCK"] = "16"

import time
import board
import busio
import adafruit_mlx90640
from adafruit_extended_bus import ExtendedI2C as I2C

# ================= GLOBALS =================
dw2_i2c_hw = None
dw2_i2c_sw = None

dw2_mlx1 = None
dw2_mlx2 = None

dw2_frame1 = None
dw2_frame2 = None

# ================= SETUP =================
def dw2_sens_setup():
    dw2_sens_therm_setup()
    print("DW2: thermal sensors setup complete")

def dw2_sens_therm_setup():
    global dw2_i2c_hw, dw2_i2c_sw
    global dw2_mlx1, dw2_mlx2
    global dw2_frame1, dw2_frame2

    # -------- Camera 1: hardware I2C (GPIO 2 / 3) --------
    dw2_i2c_hw = busio.I2C(board.SCL, board.SDA)
    dw2_mlx1 = adafruit_mlx90640.MLX90640(dw2_i2c_hw)
    dw2_mlx1.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

    # -------- Camera 2: software I2C (/dev/i2c-3) --------
    dw2_i2c_sw = I2C(3)
    dw2_mlx2 = adafruit_mlx90640.MLX90640(dw2_i2c_sw)
    dw2_mlx2.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

    dw2_frame1 = [0] * 768
    dw2_frame2 = [0] * 768

    print("DW2: initialized 2 × MLX90640")

# ================= READ =================
def dw2_sens_read():
    return dw2_sens_therm_read()

def dw2_sens_therm_read():
    global dw2_frame1, dw2_frame2

    try:
        dw2_mlx1.getFrame(dw2_frame1)
        time.sleep(0.05)   # critical for stability
        dw2_mlx2.getFrame(dw2_frame2)

        c1 = dw2_frame1[12 * 32 + 16]
        c2 = dw2_frame2[12 * 32 + 16]

        print(f"DW2 Thermal Cam 1 center: {c1:.2f} C")
        print(f"DW2 Thermal Cam 2 center: {c2:.2f} C")

        return dw2_frame1, dw2_frame2

    except Exception as e:
        print("DW2 thermal read error:", e)
        return None, None
