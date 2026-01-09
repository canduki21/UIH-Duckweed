import DW2_SENSOR_FUNCT as dw2S
import DW2_FILE_FUNCT as dw2F
import time

dw2S.dw2_sens_setup()
time.sleep(1)

dw2S.dw2_sens_read()

print("DW2: writing thermal data")
dw2F.dw2_file_therm_write()

print("DW2: repeated logging")
for i in range(4):
    time.sleep(5)
    dw2F.dw2_file_write()
