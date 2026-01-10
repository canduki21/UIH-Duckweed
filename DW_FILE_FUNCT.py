import DW_SENSOR_FUNCT as dwS
import DW_TIME_FUNCT as dwT
import pandas as pd
import os

# ---------------- GLOBALS ----------------

temp = -1
humid = -1
co2 = -1
r = -1
g = -1
b = -1
nir = -1
therm1 = -1
therm2 = -1

# ---------------- LOG FILE ----------------

file_path = 'DW_LOG.csv'


def file_connect_check():
    if os.path.isfile(file_path):
        print("Requested file is found; data will be logged.")
    else:
        print("Requested file not found; file will be created.")
    return


def file_upload(file_path, file_data):
    try:
        file_data.to_csv(file_path, mode='a', index=False, header=False)
        print("Successfully appended new row")
    except Exception as e:
        print(f"CSV append error: {e}")
    return


# ---------------------------------------------------------
# MAIN FULL SENSOR WRITE  (THIS IS THE IMPORTANT ONE)
# ---------------------------------------------------------
def file_write():
    global file_path

    # --- sensor reads ---
    temp, humid = dwS.sens_dht22_read()
    co2 = dwS.sens_mhz19_read()
    r, g, b, nir = dwS.sens_spect_read()

    # 🔴 TWO THERMAL CAMERAS
    therm1, therm2 = dwS.sens_therm_read()

    # --- time ---
    month, day, year, hr, min, sec = dwT.time_grab()

    # --- SAME FORMAT, JUST EXTENDED ---
    new_row_data = {
        'MONTH': month,
        'DAY': day,
        'YR': year,
        'HR': hr,
        'MIN': min,
        'SEC': sec,
        'TEMP': temp,
        'HUMID': humid,
        'CO2PPM': co2,
        'R': r,
        'G': g,
        'B': b,
        'NIR': nir,
        'THERM1': therm1,
        'THERM2': therm2
    }

    new_row_df = pd.DataFrame([new_row_data])
    file_upload(file_path, new_row_df)
    return new_row_df


# ---------------------------------------------------------
# SINGLE-SENSOR WRITES (UNCHANGED STYLE)
# ---------------------------------------------------------
def file_dht22_write():
    temp, humid = dwS.sens_dht22_read()
    month, day, year, hr, min, sec = dwT.time_grab()

    new_row_data = {
        'MONTH': month, 'DAY': day, 'YR': year,
        'HR': hr, 'MIN': min, 'SEC': sec,
        'TEMP': temp, 'HUMID': humid,
        'CO2PPM': 'Nan', 'R': 'Nan', 'G': 'Nan',
        'B': 'Nan', 'NIR': 'Nan',
        'THERM1': 'Nan', 'THERM2': 'Nan'
    }

    file_upload(file_path, pd.DataFrame([new_row_data]))
    return


def file_mhz19_write():
    co2 = dwS.sens_mhz19_read()
    month, day, year, hr, min, sec = dwT.time_grab()

    new_row_data = {
        'MONTH': month, 'DAY': day, 'YR': year,
        'HR': hr, 'MIN': min, 'SEC': sec,
        'TEMP': 'Nan', 'HUMID': 'Nan',
        'CO2PPM': co2,
        'R': 'Nan', 'G': 'Nan', 'B': 'Nan',
        'NIR': 'Nan',
        'THERM1': 'Nan', 'THERM2': 'Nan'
    }

    file_upload(file_path, pd.DataFrame([new_row_data]))
    return


def file_spect_write():
    r, g, b, nir = dwS.sens_spect_read()
    month, day, year, hr, min, sec = dwT.time_grab()

    new_row_data = {
        'MONTH': month, 'DAY': day, 'YR': year,
        'HR': hr, 'MIN': min, 'SEC': sec,
        'TEMP': 'Nan', 'HUMID': 'Nan',
        'CO2PPM': 'Nan',
        'R': r, 'G': g, 'B': b, 'NIR': nir,
        'THERM1': 'Nan', 'THERM2': 'Nan'
    }

    file_upload(file_path, pd.DataFrame([new_row_data]))
    return


def file_therm_write():
    therm1, therm2 = dwS.sens_therm_read()
    month, day, year, hr, min, sec = dwT.time_grab()

    new_row_data = {
        'MONTH': month, 'DAY': day, 'YR': year,
        'HR': hr, 'MIN': min, 'SEC': sec,
        'TEMP': 'Nan', 'HUMID': 'Nan',
        'CO2PPM': 'Nan',
        'R': 'Nan', 'G': 'Nan', 'B': 'Nan', 'NIR': 'Nan',
        'THERM1': therm1,
        'THERM2': therm2
    }

    file_upload(file_path, pd.DataFrame([new_row_data]))
    return
