import RPi.GPIO as GPIO
import time

ATOMIZER_PIN = 25  # GPIO25 (BCM numbering)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ATOMIZER_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    print("Atomizer ON")
    GPIO.output(ATOMIZER_PIN, GPIO.HIGH)
    time.sleep(5)

    print("Atomizer OFF")
    GPIO.output(ATOMIZER_PIN, GPIO.LOW)

finally:
    GPIO.cleanup()
