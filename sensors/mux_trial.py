#! /usr/bin/python
#Libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_MUX_EN = 12
GPIO_MUX_A = [25,8,7,1]

GPIO_TRIGGER = 23
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_MUX_EN, GPIO.OUT)
for port in GPIO_MUX_A:
    GPIO.setup(port, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def setAddress(number):
    #Check the number is in range
    if 0 <= number <= 15:
        #Iterate over each bit and check if it's set or not
        for i in range(4):
            if (number & (1<<i)):
                GPIO.output(GPIO_MUX_A[i],True)
            else:
                GPIO.output(GPIO_MUX_A[i],False)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def getSensorData(number):
    #Disable muxes first
    GPIO.output(GPIO_MUX_EN, False)
    #Set address bits
    setAddress(number)
    #Enable muxes
    GPIO.output(GPIO_MUX_EN, True)
    return distance()



if __name__ == '__main__':
    try:
       # GPIO.output(GPIO_TRIGGER, True)
        while True:
            inp = int(raw_input())
            #GPIO.output(GPIO_MUX_EN, False)
            #Set address bits
            dist = getSensorData(inp)
            #Enable muxes
            #GPIO.output(GPIO_MUX_EN, True)
            print("Sensor distance is: " + str(dist))

        # while True:
        #     dist = distance()
        #     print ("Measured Distance = %.1f cm" % dist)
        #     time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
