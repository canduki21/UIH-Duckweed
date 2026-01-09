import qwiic_as7343 
import sys
import time

def runExample():
	print("\nQwiic AS7343 Example 1 - Basic Readings\n")

	myAS7343 = qwiic_as7343.QwiicAS7343()

	if myAS7343.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	if not myAS7343.begin():
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	
	myAS7343.power_on()
	print("Device powered on")

	if not myAS7343.set_auto_smux(myAS7343.kAutoSmux18Channels):
		print("Failed to set AutoSmux", file=sys.stderr)
		return
	print("AutoSmux set to 18 channels")

	if not myAS7343.spectral_measurement_enable():
		print("Failed to enable spectral measurements", file=sys.stderr)
		return
	print("Spectral measurements enabled")

	while True:
		myAS7343.set_led_drive(0) # 0 = 4mA
		myAS7343.set_led_on()

		time.sleep(0.100) # Wait 100 ms for LED to fully illuminate our target
		
		myAS7343.read_all_spectral_data()

		myAS7343.set_led_off()

		print(myAS7343.get_blue(), end=',')
		print(myAS7343.get_red(), end=',')
		print(myAS7343.get_green(), end=',')
		print(myAS7343.get_nir(), end=',\n')

		time.sleep(0.500) # Wait 500 ms before next reading

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)
