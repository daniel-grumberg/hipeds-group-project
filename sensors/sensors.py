#! /usr/bin/python
#Libraries
import RPi.GPIO as GPIO
import time
import signal

GPIO.setmode(GPIO.BCM)

class AddressBus:
    def __init__(self, pins, enable):
        self.pins = pins
        self.address_bits = len(pins)
        self.enable = enable
        GPIO.setup(enable, GPIO.OUT)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

    def is_valid_index(self, idx):
        return (0 <= idx) and (idx.bit_length() <= self.address_bits)

    def select_index(self, idx):
        assert(self.is_valid_index(idx))
        GPIO.output(self.enable, False)
        set_bits = [ (idx >> i) & 1 for i in range(self.address_bits) ]
        for pin, value in zip(self.pins, set_bits):
            GPIO.output(pin, bool(value))
        GPIO.output(self.enable, True)

    def clear(self):
        GPIO.output(self.enable, False)
        for pin in self.pins:
            GPIO.output(pin, False)

class DepthSensor:
    GPIO_TRIGGER = 0
    GPIO_ECHO = 0

    @classmethod
    def init_gpio_pins(cls):
        GPIO.setup(cls.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(cls.GPIO_ECHO, GPIO.IN)
        # Register a handler for SIGALRM, we use this in order to implement a
        # timeout on the depth sensor in case of hardware error
        def __alarm_sig_handler(signum, frame):
            raise Exception()
        signal.signal(signal.SIGALRM, __alarm_sig_handler)

    def __init__(self, index):
        self.index = index

    # We use SIGALRM to implement timing out the sensor measurement. An
    # exception is raised by the handler, which cuts control flow into the
    # except block which leads back to the top of the while loop. When no
    # exception is raised, the function returns the measurement as expected.
    def distance(self):
        for _ in range(4):
            try:
                # set the alarm, this will cancel any previously active alarms
                signal.alarm(1)
                # set Trigger to HIGH
                GPIO.output(self.GPIO_TRIGGER, True)

                # set Trigger after 0.01ms to LOW
                time.sleep(0.00001)

                GPIO.output(self.GPIO_TRIGGER, False)

                start_time = time.time()

                stop_time = time.time()

                # save start_time
                while GPIO.input(self.GPIO_ECHO) == 0:
                    start_time = time.time()


                # save time of arrival
                while GPIO.input(self.GPIO_ECHO) == 1:
                    stop_time = time.time()


                # time difference between start and arrival
                TimeElapsed = stop_time - start_time

                # multiply with the sonic speed (34300 cm/s)
                # and divide by 2, because there and back
                distance = (TimeElapsed * 34300) / 2

                # if we return before the alarm trigerred, so cancel it
                signal.alarm(0)
                return distance
            except Exception:
                pass
        signal.alarm(0)
        return -1

if __name__ == '__main__':
    try:
        DepthSensor.GPIO_TRIGGER = 23
        DepthSensor.GPIO_ECHO = 24

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
