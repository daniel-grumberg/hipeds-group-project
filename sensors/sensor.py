#! /usr/bin/python
#Libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class AddressBus:
    def __init__(self, pins):
        self.pins = pins
        self.address_bits = len(pins)
        for pin in self.bits:
            GPIO.setup(pin, GPIO.OUT)

    def is_valid_index(self, idx):
        return (0 <= idx) and (idx.bit_length() <= self.address_bits)
class DepthSensor:
    GPIO_TRIGGER = 0
    GPIO_ECHO = 0
    address_bus = []

    @classmethod
    def init_gpio_pins(cls):
        GPIO.setup(cls.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(cls.GPIO_ECHO, GPIO.IN)

    def __init__(self, index):
        assert(address_bus.is_valid_index(index))
        self.index = index

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        # save start_time
        while GPIO.input(GPIO_ECHO) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        TimeElapsed = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

if __name__ == '__main__':
    class DummyAddressBus:
        def is_valid_index(idx):
            return True

    try:
        DepthSensor.GPIO_TRIGGER = 23
        DepthSensor.GPIO_ECHO = 23
        DepthSensor.address_bus = DummyAddressBus()

        DepthSensor.init_gpio_pins()

        sensor = DepthSensor(0)
        while True:
            dist = sensor.distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup() 
