#!/usr/bin/python3


'''

This code offers some utility functions for retrieving/updating 
sensor values on the Amazon AWS database

'''

import pymysql
import time



'''
	Useful lambda function for calculating current time in milli-seconds
'''
current_milli_time = lambda: int(round(time.time() * 1000))


host_name = "hipeds-group.ckjqazo6ukkn.eu-west-2.rds.amazonaws.com"
db_username = "hipeds"
db_password = "YHADXjMrX3nGssAw"
db_name = "innodb" 	

class aws_db:
	
	def __init__(self):
		print("Connecting to aws database...")
		#try:
		self.db = pymysql.connect(host_name, db_username, db_password, db_name)
		self.cur = self.db.cursor()
		#except:
		#	print("Failed to connect")
	
	'''
		Add sensor reading
	'''
	def add_reading(self, readings):
		for sensorId, value in readings:
			sql = "INSERT INTO DepthSensorReadings (sensorId, value, timestamp) VALUES (%s, %s, %s)" % (sensorId, value, current_milli_time());
			print("EXECUTING ---> " + sql)
			self.cur.execute(sql)

	'''
		This function will raise an error, if unable to connect to the database
	'''
	def check_con(self):
		self.cur.execute("SELECT VERSION()")
		data = self.cur.fetchone()
		print("Database version : %s " % data)
		
	'''
		Return the most recent sensor reading for a list of sensors
	'''
	def get_last_readings(self, sensorIds):
		# The below method can return multiple readings from one sensor, as opposed to getting at least one from each
		#sql = "SELECT * FROM DepthSensorReadings WHERE sensorId IN (%s) ORDER BY timestamp DESC" % ",".join(map(str, sensorIds));
		#print("EXECUTING ---> " + sql)
		#cur.execute(sql)
		
		data = []
		for sensorId in sensorIds:
			sql = "SELECT * FROM DepthSensorReadings WHERE sensorId = %s ORDER BY timestamp DESC LIMIT 1" % sensorId
			print("EXECUTING ---> " + sql)
			self.cur.execute(sql)
			data.append(self.cur.fetchall())
			
		print(data)
		return data
		
	'''
		Deletes all the previous depth sensor readings and resets the PK
	'''
	def delete_previous_readings(self):
		self.cur.execute("TRUNCATE TABLE DepthSensorReadings")
		
	'''
		Deletes all the sensors ids
	'''
	def delete_sensors(self):
		self.cur.execute("TRUNCATE TABLE DepthSensors")
		
	'''
		List the Ids of all the sensors
	'''
	def get_sensor_ids(self):
		self.cur.execute("SELECT idDepthSensors From DepthSensors")
		result = self.cur.fetchall()
		print(result)
		return result
		
	'''
		Add a list of sensor ids
	'''
	def add_sensors(self, sensorIds):
		for id in sensorIds: # Ideally in a single query..
			sql = "INSERT INTO DepthSensors (idDepthSensors) VALUES (%s)" % id;
			print("EXECUTING ---> " + sql)
			self.cur.execute(sql)
			
			
	def update_ip(self, new_ip):
		sql = "INSERT INTO IpAddresses (IpAddress, timestamp) VALUES ('%s', %s)" % (new_ip, current_milli_time());
		print("EXECUTING ---> " + sql)
		self.cur.execute(sql)
	
	def get_last_ip(self):
		sql = "SELECT IpAddress FROM IpAddresses ORDER BY timestamp DESC LIMIT 1"
		print("EXECUTING ---> " + sql)
		self.cur.execute(sql)
		last_ip = self.cur.fetchone()
		
		if last_ip is None:
			print("No last known ip")
		else:
			#print("Last ip address = " + last_ip)
			print(last_ip)
			
		return last_ip
	
			
	def close(self):
		self.db.close()

'''
	Unit test
'''
def test():
	db = aws_db()

	db.check_con()

	'''db.delete_previous_readings()
	db.delete_sensors()
	db.add_sensors([1,2,3,4]) # 4 Sensors
	db.get_sensor_ids()

	db.get_last_readings([1,2,3,4])

	# sensorId must be a valid Id from DepthSensors, else will fail foreign key constraint
	sensorIds = [1]
	readings = [(1, 8)]
	db.add_reading(readings)
	db.get_last_readings(sensorIds)
	db.delete_previous_readings()'''
	
	db.get_last_ip()
	db.update_ip("192.168.blah")
	db.get_last_ip()
	db.update_ip("192.168.blah2")
	db.get_last_ip()

	db.close()
	
	
# Call unit test
test()