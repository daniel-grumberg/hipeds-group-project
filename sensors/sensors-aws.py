#!/usr/bin/python3


'''

This code offers some utility functions for retrieving/updating 
sensor values on the Amazon AWS database

'''

import pymysql
import time

host_name = "hipeds-group.ckjqazo6ukkn.eu-west-2.rds.amazonaws.com"
db_username = "hipeds"
db_password = "YHADXjMrX3nGssAw"
db_name = "innodb" 	
	
# Open database connection
db = pymysql.connect(host_name, db_username, db_password, db_name)
cur = db.cursor()

current_milli_time = lambda: int(round(time.time() * 1000))

# Utility fuctions

#ALTER TABLE DepthSensorReadings
#ADD FOREIGN KEY (sensorId) REFERENCES DepthSensors(idDepthSensors);

'''
	Add sensor reading
'''
def add_reading(readings):
	for sensorId, value in readings:
		sql = "INSERT INTO DepthSensorReadings (sensorId, value, timestamp) VALUES (%s, %s, %s)" % (sensorId, value, current_milli_time());
		print("EXECUTING ---> " + sql)
		cur.execute(sql)

'''
	This function will raise an error, if unable to connect to the database
'''
def check_con():
	cur.execute("SELECT VERSION()")
	data = cur.fetchone()
	print("Database version : %s " % data)
	
'''
	Return the most recent sensor reading for a list of sensors
'''
def get_last_readings(sensorIds):
	# The below method can return multiple readings from one sensor, as opposed to getting at least one from each
	#sql = "SELECT * FROM DepthSensorReadings WHERE sensorId IN (%s) ORDER BY timestamp DESC" % ",".join(map(str, sensorIds));
	#print("EXECUTING ---> " + sql)
	#cur.execute(sql)
	
	data = []
	for sensorId in sensorIds:
		sql = "SELECT * FROM DepthSensorReadings WHERE sensorId = %s ORDER BY timestamp DESC LIMIT 1" % sensorId
		print("EXECUTING ---> " + sql)
		cur.execute(sql)
		data.append(cur.fetchall())
		
	print(data)
	return data
	
'''
	Deletes all the previous depth sensor readings and resets the PK
'''
def delete_previous_readings():
	cur.execute("TRUNCATE TABLE DepthSensorReadings")
	
'''
	Deletes all the sensors ids
'''
def delete_sensors():
	cur.execute("TRUNCATE TABLE DepthSensors")
	
'''
	List the Ids of all the sensors
'''
def get_sensor_ids():
	cur.execute("SELECT idDepthSensors From DepthSensors")
	result = cur.fetchall()
	print(result)
	return result
	
'''
	Add a list of sensor ids
'''
def add_sensors(sensorIds):
	for id in sensorIds: # Ideally in a single query..
		sql = "INSERT INTO DepthSensors (idDepthSensors) VALUES (%s)" % id;
		print("EXECUTING ---> " + sql)
		cur.execute(sql)

# End utility functions

check_con()

delete_previous_readings()
delete_sensors()
add_sensors([1,2,3,4]) # 4 Sensors
get_sensor_ids()

get_last_readings([1,2,3,4])

# sensorId must be a valid Id from DepthSensors, else will fail foreign key constraint
sensorIds = [1]
readings = [(1, 8)]
add_reading(readings)
get_last_readings(sensorIds)
delete_previous_readings()

db.close()