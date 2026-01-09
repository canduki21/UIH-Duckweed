import time
import csv
import os
import DW2_SENSOR_FUNCT as dw2S

DW2_THERM_FILE = "dw2_thermal_log.csv"

# ================= THERMAL FILE WRITE =================
def dw2_file_therm_write():
    frame1, frame2 = dw2S.dw2_sens_therm_read()

    if frame1 is None or frame2 is None:
        print("DW2: thermal data unavailable")
        return

    timestamp = time.time()
    file_exists = os.path.isfile(DW2_THERM_FILE)

    with open(DW2_THERM_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        # Write header once
        if not file_exists:
            header = (
                ["timestamp"] +
                [f"dw2_cam1_px{i}" for i in range(768)] +
                [f"dw2_cam2_px{i}" for i in range(768)]
            )
            writer.writerow(header)

        writer.writerow([timestamp] + frame1 + frame2)

    print("DW2: thermal data written")

# ================= COMBINED WRITE =================
def dw2_file_write():
    dw2_file_therm_write()
