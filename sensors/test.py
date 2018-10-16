#! /usr/bin/python

import sensors
import time

sensor_map = {0: 5, 1: 15, 2: 14, 3: 13, 4: 12, 5: 11, 6: 10, 7: 9, 8: 8, 9: 7,
                10: 6, 11: 0, 12: 4, 13: 3, 14: 2, 15: 1}

def init_depth_sensors():
    sensors.DepthSensor.GPIO_TRIGGER = 23
    sensors.DepthSensor.GPIO_ECHO = 24
    sensors.DepthSensor.init_gpio_pins()

if __name__ == "__main__":
    init_depth_sensors()
    bus = sensors.AddressBus([25, 8, 7, 1], 12)
    for i in range(16):
        depth_sensor = sensors.DepthSensor(sensor_map[i])
        bus.select_index(depth_sensor.index)
        measurement = depth_sensor.distance()
        print "Sensor #{0} measured:{1}".format(sensor_map[depth_sensor.index], measurement)
    bus.clear()
    sensors.GPIO.cleanup()
