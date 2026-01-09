import os
os.environ["BLINKA_MLX90640_FORCE_BLOCK"] = "16"

import time
import numpy as np
import matplotlib.pyplot as plt
import board
import busio
import adafruit_mlx90640
from adafruit_extended_bus import ExtendedI2C as I2C

---------------- I2C ----------------
Camera 1: hardware I2C (GPIO 2 / 3)
i2c_hw = busio.I2C(board.SCL, board.SDA, frequency=400000)

Camera 2: software I2C (GPIO 23 / 24 → /dev/i2c-3)
i2c_sw = I2C(3)

---------------- Sensors ----------------
mlx1 = adafruit_mlx90640.MLX90640(i2c_hw)
mlx2 = adafruit_mlx90640.MLX90640(i2c_sw)

mlx1.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
mlx2.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

frame1 = [0] * 768
frame2 = [0] * 768

---------------- Plot ----------------
plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

img1 = ax1.imshow(
    np.zeros((24, 32)),
    cmap='inferno',
    vmin=15,
    vmax=40,
    interpolation='nearest'
)
img2 = ax2.imshow(
    np.zeros((24, 32)),
    cmap='inferno',
    vmin=15,
    vmax=40,
    interpolation='nearest'
)

plt.colorbar(img1, ax=ax1)
plt.colorbar(img2, ax=ax2)

ax1.set_title("MLX90640 Camera 1")
ax2.set_title("MLX90640 Camera 2")

---------------- Loop ----------------
while True:
    try:
        mlx1.getFrame(frame1)
        time.sleep(0.05)  # IMPORTANT: avoid bus contention
        mlx2.getFrame(frame2)

        img1.set_data(np.reshape(frame1, (24, 32)))
        img2.set_data(np.reshape(frame2, (24, 32)))

        plt.pause(0.05)

    except Exception as e:
        print("Frame error:", e)
        time.sleep(0.2)
