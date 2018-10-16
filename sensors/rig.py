#! /usr/bin/python

import argparse as argp
import sensors
import time
import json

def compute_free_space(measurements, w, d, h):
    van_volume = w * d * h
    sensor_area = (1.0 / 15.0) * w * d
    free_volume = 0
    assert(len(measurements) == 15)
    for m in measurements:
        free_volume += m * sensor_area
    space_fmt = "The proportion of free space is {0} / {1} = {2}"
    print space_fmt.format(float(free_volume), float(van_volume), (float(free_volume)/float(van_volume)))


sensor_map = {0: 5, 1: 15, 2: 14, 3: 13, 4: 12, 5: 11, 6: 10, 7: 9, 8: 8, 9: 7,
                10: 6, 11: 0, 12: 4, 13: 3, 14: 2, 15: 1}

def init_depth_sensors():
    sensors.DepthSensor.GPIO_TRIGGER = 23
    sensors.DepthSensor.GPIO_ECHO = 24
    sensors.DepthSensor.init_gpio_pins()

if __name__ == "__main__":
    arg_parser = argp.ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=argp.FileType('w'))
    args = arg_parser.parse_args()

    try:
        init_depth_sensors()
        bus = sensors.AddressBus([25, 8, 7, 1], 12)

        depth_sensors = []
        for idx in range(1 << bus.address_bits):
            depth_sensors.append(sensors.DepthSensor(idx))

        while True:
            measurements = []
            for s in depth_sensors:
                if s.index == 11:
                    continue
                bus.select_index(s.index)
                value = s.distance()
                measurements.append(value)
                print "Sensor #{0} measured: {1}".format(sensor_map[s.index], value)
            compute_free_space(measurements, 100, 180, 105)
            if args.file != None:
                args.file.truncate(0)
                args.file.seek(0)
                json.dump(measurements, args.file)
            time.sleep(5)

    except KeyboardInterrupt:
        print "Measurement stopped by user"
        bus.clear()
        sensors.GPIO.cleanup()
        if args.file != None:
            args.file.close()
