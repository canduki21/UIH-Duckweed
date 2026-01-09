import time
import csv
import os
import DW2_SENSOR_FUNCT as dw2S

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "DW2_LOG.csv")

def dw2_file_write():
    data = dw2S.dw2_sens_read()

    if data["thermal"][0] is None:
        print("DW2: skipping write (thermal error)")
        return

    row = [
        time.time(),
        *data["dht"],
        data["co2"],
        *data["spect"],
        *data["thermal"][0],
        *data["thermal"][1]
    ]

    write_header = not os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            header = (
                ["timestamp","temp","humidity","co2",
                 "blue","green","red","nir"] +
                [f"cam1_px{i}" for i in range(768)] +
                [f"cam2_px{i}" for i in range(768)]
            )
            w.writerow(header)
        w.writerow(row)

    print("DW2: data written")
