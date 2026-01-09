import sys
import time
import os
import numpy as np

# ================= PyQt =================
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap

# ================= Matplotlib =================
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# ================= OpenCV =================
import cv2

# ================= Sensors =================
import DW_SENSOR_FUNCT as dwS
import DW_FILE_FUNCT as dwF

import board
import busio
import adafruit_mlx90640
from adafruit_extended_bus import ExtendedI2C as I2C

os.environ["BLINKA_MLX90640_FORCE_BLOCK"] = "16"


# ============================================================
# Thermal Camera Worker
# ============================================================
class ThermalWorker(QThread):
    frame_signal = pyqtSignal(np.ndarray, np.ndarray)
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True

        self.i2c_hw = busio.I2C(board.SCL, board.SDA, frequency=400000)
        self.i2c_sw = I2C(3)

        self.mlx1 = adafruit_mlx90640.MLX90640(self.i2c_hw)
        self.mlx2 = adafruit_mlx90640.MLX90640(self.i2c_sw)

        self.mlx1.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
        self.mlx2.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

        self.frame1 = [0] * 768
        self.frame2 = [0] * 768

    def run(self):
        self.log_signal.emit("Thermal cameras started")

        while self.running:
            try:
                self.mlx1.getFrame(self.frame1)
                time.sleep(0.05)
                self.mlx2.getFrame(self.frame2)

                f1 = np.reshape(self.frame1, (24, 32))
                f2 = np.reshape(self.frame2, (24, 32))

                self.frame_signal.emit(f1, f2)

            except Exception as e:
                self.log_signal.emit(f"Thermal error: {e}")
                time.sleep(0.2)

        self.log_signal.emit("Thermal cameras stopped")

    def stop(self):
        self.running = False
        self.wait()


# ============================================================
# Thermal Plot Canvas
# ============================================================
class ThermalCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(8, 4))
        self.ax1, self.ax2 = self.fig.subplots(1, 2)
        super().__init__(self.fig)

        self.img1 = self.ax1.imshow(
            np.zeros((24, 32)),
            cmap="inferno",
            vmin=15, vmax=40,
            interpolation="nearest"
        )
        self.img2 = self.ax2.imshow(
            np.zeros((24, 32)),
            cmap="inferno",
            vmin=15, vmax=40,
            interpolation="nearest"
        )

        self.ax1.set_title("MLX90640 Camera 1")
        self.ax2.set_title("MLX90640 Camera 2")

        self.fig.colorbar(self.img1, ax=self.ax1)
        self.fig.colorbar(self.img2, ax=self.ax2)

    def update_frames(self, f1, f2):
        self.img1.set_data(f1)
        self.img2.set_data(f2)
        self.draw_idle()


# ============================================================
# Main GUI
# ============================================================
class DuckweedGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Duckweed – Full Sensor GUI")
        self.resize(1200, 750)

        # ---------- Widgets ----------
        self.canvas = ThermalCanvas()
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        self.usb_cam_label = QLabel("Waiting for snapshot…")
        self.usb_cam_label.setFixedSize(320, 240)
        self.usb_cam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.usb_cam_label.setStyleSheet("background-color: black; color: white;")

        self.temp_label = QLabel("Temp: -- °C")
        self.hum_label = QLabel("Humidity: -- %")
        self.temp_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.hum_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.btn_init = QPushButton("Initialize Sensors")
        self.btn_read = QPushButton("Read Sensors")
        self.btn_write = QPushButton("Write Sensors to File")
        self.btn_start_thermal = QPushButton("Start Thermal Cameras")
        self.btn_stop_thermal = QPushButton("Stop Thermal Cameras")

        # ---------- Layout ----------
        top_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Thermal Cameras"))
        left_layout.addWidget(self.canvas)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("USB Camera Snapshot (every 2.5 min)"))
        right_layout.addWidget(self.usb_cam_label)
        right_layout.addWidget(self.temp_label)
        right_layout.addWidget(self.hum_label)
        right_layout.addStretch()

        top_layout.addLayout(left_layout, 3)
        top_layout.addLayout(right_layout, 1)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_init)
        btn_layout.addWidget(self.btn_read)
        btn_layout.addWidget(self.btn_write)

        thermal_btn_layout = QHBoxLayout()
        thermal_btn_layout.addWidget(self.btn_start_thermal)
        thermal_btn_layout.addWidget(self.btn_stop_thermal)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(thermal_btn_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(QLabel("System Log"))
        main_layout.addWidget(self.log_box)

        self.setLayout(main_layout)

        # ---------- Connections ----------
        self.btn_init.clicked.connect(self.init_sensors)
        self.btn_read.clicked.connect(self.read_sensors)
        self.btn_write.clicked.connect(self.write_files)
        self.btn_start_thermal.clicked.connect(self.start_thermal)
        self.btn_stop_thermal.clicked.connect(self.stop_thermal)

        # ---------- Workers ----------
        self.thermal_worker = None

        # ---------- USB snapshot timer ----------
        self.cap = cv2.VideoCapture(0)
        self.snapshot_timer = QTimer()
        self.snapshot_timer.timeout.connect(self.take_snapshot)
        self.snapshot_timer.start(150_000)  # 2.5 minutes

        self.log("USB camera snapshot timer started (2.5 min interval)")

    # ========================================================
    # Actions
    # ========================================================
    def log(self, text):
        self.log_box.append(text)

    def init_sensors(self):
        self.log("Initializing sensors...")
        dwS.sens_setup()
        self.log("Sensors initialized")

    def read_sensors(self):
        self.log("Reading sensors...")
        dwS.sens_read()

        try:
            self.temp_label.setText(f"Temp: {dwS.last_temp:.1f} °C")
            self.hum_label.setText(f"Humidity: {dwS.last_humidity:.1f} %")
        except:
            pass

        self.log("Sensor read complete")

    def write_files(self):
        self.log("Writing sensor data to files...")
        dwF.file_write()
        self.log("Files written")

    def start_thermal(self):
        if self.thermal_worker is None:
            self.thermal_worker = ThermalWorker()
            self.thermal_worker.frame_signal.connect(self.canvas.update_frames)
            self.thermal_worker.log_signal.connect(self.log)
            self.thermal_worker.start()

    def stop_thermal(self):
        if self.thermal_worker:
            self.thermal_worker.stop()
            self.thermal_worker = None

    # ========================================================
    # USB snapshot
    # ========================================================
    def take_snapshot(self):
        if not self.cap.isOpened():
            self.log("USB camera not available")
            return

        ret, frame = self.cap.read()
        if not ret:
            self.log("Failed to capture USB snapshot")
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)

        pixmap = QPixmap.fromImage(img).scaled(
            self.usb_cam_label.width(),
            self.usb_cam_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

        self.usb_cam_label.setPixmap(pixmap)
        self.log("USB snapshot captured")

    # ========================================================
    # Cleanup
    # ========================================================
    def closeEvent(self, event):
        if self.thermal_worker:
            self.thermal_worker.stop()
        if self.cap:
            self.cap.release()
        event.accept()


# ============================================================
# Run
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = DuckweedGUI()
    gui.show()
    sys.exit(app.exec())
