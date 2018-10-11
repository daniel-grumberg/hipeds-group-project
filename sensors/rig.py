#! /usr/bin/python

import sensors

def init_depth_sensors():
    sensors.DepthSensor.GPIO_TRIGGER = 23
    sensors.DepthSensor.GPIO_ECHO = 24
    sensors.DepthSensor.init_gpio_pins()

if __name__ == "__main__":
    try:
        init_depth_sensors()
        bus = sensors.AddressBus([25, 8, 7, 1], 12)

        depth_sensors = []
        for idx in range(1 << bus.address_bits):
            depth_sensors.append(sensors.DepthSensor(idx))

        while True:
            for s in depth_sensors:
                bus.select_index(s.index)
                measurement = s.distance()
                print "Sensor #{0} measured: {1}".format(s.index, measurement)
    except KeyboardInterrupt:
        print "Measurement stopped by user"
        bus.clear()
        sensors.GPIO.cleanup()
