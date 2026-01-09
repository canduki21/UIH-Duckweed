from gpiozero import DigitalOutputDevice
from time import sleep

# GPIO 25 -> 220Ω -> MOSFET Gate
atomizer = DigitalOutputDevice(25, active_high=True, initial_value=False)

try:
    print("Atomizer ON")
    atomizer.on()
    sleep(3)

    print("Atomizer OFF")
    atomizer.off()
    sleep(2)

    # Pulse test (recommended)
    for i in range(5):
        atomizer.on()
        sleep(0.5)
        atomizer.off()
        sleep(0.5)

finally:
    atomizer.off()
    atomizer.close()
