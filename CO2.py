import serial
import time

READ_INTERVAL_SECONDS = 0.5
SERIAL_PORT_NAME = "/dev/ttyAMA0"
SERIAL_PORT_BAUD_RATE = 9600

# ser = serial.Serial('/dev/ttyAMA10',9600, timeout=1)
ser = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUD_RATE, timeout=1)

cmd = bytearray ([0xFF, 0X01, 0X86, 0 ,0, 0, 0, 0, 0X79])

while True :
	ser.write(cmd)
	resp = ser.read(9)

	if len(resp) == 9 and resp[0] == 0xFF and resp[1] == 0x86:
		co2 = resp[2] * 256 + resp[3]
		print ("CO2:", co2, "ppm")
		print ("Response length (bytes):", len(resp))
		print ("Raw response:", resp)
		print ("")
	else:
		print("invalid response:", resp)

	time.sleep(READ_INTERVAL_SECONDS)
