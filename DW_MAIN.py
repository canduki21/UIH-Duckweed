#from DW_SENSOR_FUNCT import sens_setup, sens_read
import DW_SENSOR_FUNCT as dwS
import DW_FILE_FUNCT as dwF
import DW_TIME_FUNCT as dwT
import time
#sens_dht22_setup()
#sens_mhz19_setup()
#sens_spect_setup()
#sens_therm_setup()

#sens_dht22_read()
#sens_mhz19_read()
#sens_spect_read()
#sens_therm_read()

dwS.sens_setup()
time.sleep(1)

dwS.sens_read()

print("testing file functions for component reading in 3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
time.sleep(1)
print("Read dht22:")
dwF.file_dht22_write()
print("Read mhz19:")
dwF.file_mhz19_write()
print("Read spect:")
dwF.file_spect_write()
print("Read therm:")
dwF.file_therm_write()

print("Testing 4 sensor reads and file writes in 20 seconds:")
for i in range(4):
    time.sleep(5)
    dwF.file_write()
