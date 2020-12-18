import time
import RPi.GPIO as GPIO

class GPIOOperationsProvider():
    def __init__(self):
        self.__relay_controller_pin = 7
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__relay_controller_pin, GPIO.OUT)

    def trigger_relay(self, delay):
        GPIO.output(self.__relay_controller_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.__relay_controller_pin, GPIO.LOW)