#GPIO setup

import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
#PLEASE UPDATE PINS, check
# LED control pin (gate of MOSFET via R_Gate)
LED_CTRL_PIN = 18  

# fan control pins these drive the MOSFETs for the fans
FAN1_CTRL_PIN = 23
FAN2_CTRL_PIN = 24

# Piezo control pin  drives the piezo transducer
PIEZO_CTRL_PIN = 25







#LED PWM DRIVER

# SSet up LED control pin as output
GPIO.setup(LED_CTRL_PIN, GPIO.OUT)


led_pwm = GPIO.PWM(LED_CTRL_PIN, 500) #500 FOR DIM, CHANGE IF NEED

led_pwm.start(0)






##THIS IS JUST FOR TEST, COMMENT OUT IF NEEDED
"""
def set_led_brightness(percent):
    
 
    
    percent = max(0, min(100, percent))  # Clamp to [0,100]
    led_pwm.ChangeDutyCycle(percent)
    """
    
    
#fan CONTROL
# Set up fan pins as outputs
GPIO.setup(FAN1_CTRL_PIN, GPIO.OUT)
GPIO.setup(FAN2_CTRL_PIN, GPIO.OUT)

def fan_on(fan_pin):
    GPIO.output(fan_pin, GPIO.HIGH)

def fan_off(fan_pin):
    GPIO.output(fan_pin, GPIO.LOW)

# THIS IS FOR PWM for fan speed control I FNEEDED
fan1_pwm = GPIO.PWM(FAN1_CTRL_PIN, 25000)  # 25 kHz typical for DC fans
fan2_pwm = GPIO.PWM(FAN2_CTRL_PIN, 25000)
fan1_pwm.start(0)
fan2_pwm.start(0)

def set_fan_speed(fan_pwm, percent):
    percent = max(0, min(100, percent))
    fan_pwm.ChangeDutyCycle(percent)
    
    
    
    
    
    
#PIEZO DRIVER
# Set up piezo pin as output
GPIO.setup(PIEZO_CTRL_PIN, GPIO.OUT)


piezo_pwm = GPIO.PWM(PIEZO_CTRL_PIN, 2000) #FOR DESIRED FREQ

def start_piezo(frequency_hz):
    
    piezo_pwm.ChangeFrequency(frequency_hz)
    piezo_pwm.start(50) #% OF DUTY CYCCLE

def stop_piezo():
 
    piezo_pwm.stop()
    GPIO.output(PIEZO_CTRL_PIN, GPIO.LOW)
    





#FOR CLEANUP AFTER RUNN
def cleanup():
    led_pwm.stop()
    fan1_pwm.stop()
    fan2_pwm.stop()
    piezo_pwm.stop()
  
    GPIO.cleanup() # this res all GPIOs