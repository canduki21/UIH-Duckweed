import DW2_SENSOR_FUNCT as dw2S
import DW2_FILE_FUNCT as dw2F
import time

dw2S.dw2_sens_setup()
time.sleep(1)

for i in range(4):
    dw2F.dw2_file_write()
    time.sleep(5)
