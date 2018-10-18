import numpy as np
import json, sys, os

results_dir = sys.argv[1]

try:
	empty_file = sys.argv[2]
except:
	empty_file = '../results/17oct/empty_calib.json'

f_names = [results_dir + "/" + f for f in os.listdir(results_dir) if ".json" in
        f and "empty" not in f]

sensor_order = [5, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 4, 3, 2, 1]

with open(empty_file, 'r') as f:
	all_measurements = json.loads(f.read())

empty_readings = {}
for measurements in all_measurements:
	for i in range(len(measurements)):
		if sensor_order[i] not in empty_readings:
			empty_readings[sensor_order[i]] = [measurements[i]]
		else:
			empty_readings[sensor_order[i]].append(measurements[i])

baseline_values = {}
for sensor in empty_readings:
	baseline_values[sensor] = np.mean(empty_readings[sensor])

for f_name in f_names:

		print(f_name)

		with open(f_name, 'r') as f:

				all_trials = json.loads(f.read())

				trial_percentages = []
				sensor_readings = {}

				for measurements in all_trials:

					# calculate percent full for each trial
					sensor_percentages = []
					for i in range(len(measurements)):
						empty_percentage = measurements[i] / baseline_values[sensor_order[i]]
						sensor_percentages.append(1-empty_percentage)

					# percent full is average of each sensor percentage
					trial_percentages.append(np.mean(sensor_percentages))

				for i in range(len(trial_percentages)):
					print("Trial " + str(i+1) + ": " + str(trial_percentages[i]))

		percentage_full = np.round(np.mean(trial_percentages), 2)*100
		print("Average: " + str(int(percentage_full)) + "% full \n")


