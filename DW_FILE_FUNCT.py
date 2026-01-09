import DW_SENSOR_FUNCT as dwS
import DW_TIME_FUNCT as dwT
import pandas as pd
import os

# DEFINING GLOBALS

temp = -1
humid = -1
co2 =-1
r = -1
g = -1
b = -1
nir = -1
frame = None

# DEFINING LOG FILE

file_path = 'DW_LOG.csv'


'''
# ABSTRACT - file_connect_check()
# - Does a quick scan of the local directory to determine the file_path
#   of interest truly exists. As of now (01/06/2026) there is no flag
#   to prevent users from continuing to log their data; it will just
#   cause the creation of the location specified by the global file_path.
#
'''
def file_connect_check():
    if os.path.isfile(file_path):
        print("Requested file is found; data will be logged at location specified.")
    else:
        print("Requested file is not found; file will be created at location specified.")
        print("Otherwise, please check the program/directory to confirm chosen file.")
    return

'''
# ABSTRACT - file_upload(file_path, file_data)
# - This function takes a globally-specified file path (for us,
#   that will likely remain DW_LOG.csv) and a locally created
#   file_data csv row by the functions below and attempts to load
#   them into the csv file, with an exception present in case
#   something goes awry.
#
'''
def file_upload(file_path, file_data):
    try:
        file_data.to_csv(file_path, mode='a', index=False, header=False)
        print("Successfully appended a new row to {file_path}")
    except Exception as e:
        print(f"An error occurred during append: {e}")
    return

'''
# ABSTRACT - file_write()
# - This function takes the read data by utilizing functions written
#   in DW_SENS_FUNCT.py, and outputs them using the pandas library
#   to csv format to DW_LOG.csv. It also makes use of the 
#   DW_TIME_FUNCT.py file to obtain time in EST. The functions
#   underneath file_write() perform similarly, just for specific
#   sensors, with Nan "Not a number" as the output for the others,
#   allowing us to know when people make specific checks when the
#   logs are checked later. 
#
'''
def file_write():
    global file_path
    temp, humid = dwS.sens_dht22_read()
    co2 = dwS.sens_mhz19_read()
    r, g, b, nir = dwS.sens_spect_read()
    frame = dwS.sens_therm_read()
    
    month, day, year, hr, min, sec = dwT.time_grab()
    
    new_row_data = {'MONTH': month, 'DAY': day, 'YR': year, 'HR': hr, 'MIN': min, 'SEC': sec, 'TEMP': temp, 'HUMID': humid, 'CO2PPM': co2, 'R': r, 'G': g, 'B': b, 'NIR': nir}
    new_row_df = pd.DataFrame([new_row_data])

    file_upload(file_path,new_row_df)
    return

def file_dht22_write():
    global file_path
    temp, humid = dwS.sens_dht22_read()
    month, day, year, hr, min, sec = dwT.time_grab()
    new_row_data = {'MONTH': month, 'DAY': day, 'YR': year, 'HR': hr, 'MIN': min, 'SEC': sec, 'TEMP': temp, 'HUMID': humid, 'CO2PPM':'Nan', 'R':'Nan', 'G':'Nan', 'B':'Nan', 'NIR':'Nan' }
    new_row_df = pd.DataFrame([new_row_data])
    
    file_upload(file_path,new_row_df)
    return

def file_mhz19_write():
    co2 = dwS.sens_mhz19_read()
    #print(co2)
    month, day, year, hr, min, sec = dwT.time_grab()
    new_row_data = {'MONTH': month, 'DAY': day, 'YR': year, 'HR': hr, 'MIN': min, 'SEC': sec, 'TEMP': 'Nan', 'HUMID': 'Nan', 'CO2PPM':co2, 'R':'Nan', 'G':'Nan', 'B':'Nan', 'NIR':'Nan' }
    new_row_df = pd.DataFrame([new_row_data])
    
    file_upload(file_path,new_row_df)
    return

def file_spect_write():
    r, g, b, nir = dwS.sens_spect_read()
    #print(r) #print(g) #print(b) #print(nir)
    
    month, day, year, hr, min, sec = dwT.time_grab()
    new_row_data = {'MONTH': month, 'DAY': day, 'YR': year, 'HR': hr, 'MIN': min, 'SEC': sec, 'TEMP': 'Nan', 'HUMID': 'Nan', 'CO2PPM':'Nan', 'R':r, 'G':g, 'B':b, 'NIR':'Nan' }
    new_row_df = pd.DataFrame([new_row_data])
    
    file_upload(file_path,new_row_df)
    
    return


#DEBUG ME!!! Need to determine how we'll handle the plot data created by the thermal sensor.
def file_therm_write():
    frame = dwS.sens_therm_read()
    print("Test therm print start")
    print(frame)
    print("Test therm print end")
    return


'''

if __name__ == '__main__':
    try:
        file_connect_check()
        dwS.sens_setup()
        file_write()
        #file_dht22_write()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending Test")
        sys.exit(0)


'''
