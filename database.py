import sqlite3
from datetime import *
from dateutil import tz

db_file = 'weather.db'
variables = ['air_temp', 'ground_temp', 'soil_moisture', 'precip', 'snow_depth', 'snow_fall', 'albedo', 'orography']

def create_tables():
	conn=sqlite3.connect(db_file)
	c=conn.cursor()
	c.execute('''CREATE TABLE location (id integer primary key, name text, lat real, lon real, elevation real, UNIQUE (name) )''')
	c.execute('''CREATE TABLE measurement (id integer primary key,
	loc_id integer,
	day date,
	air_temp real,
	ground_temp real,
	soil_moisture real,
	precip real,
	snow_depth real,
	snow_fall real,
	albedo real,
	orography real,
	FOREIGN KEY(loc_id) REFERENCES location(id),
	UNIQUE(loc_id, day))''')
	conn.commit()
	conn.close()

# Standard locations:
# Overall Falls:  38.783360, -78.295143
# Lewis Spring Falls:  38.520638, -78.450539
# White oak canyon: 38.555984, -78.353889
# Finley's Folly: 37.911125, -78.973633
def add_dc_locs():
	add_location('Overall Falls', 38.783360, -78.295143, 330.32)
	add_location('Lewis Spring Falls', 38.520638, -78.450539, 437.57)
	add_location('White oak canyon', 38.555984, -78.353889, 436.07)
	add_location('Finleys Folly', 37.911125, -78.973633, 488.57)

def get_locs():
	conn=sqlite3.connect(db_file)
	c=conn.cursor()
	locs=[]
	for row in c.execute("SELECT name, lat, lon, id FROM location"):
		locs.append({'name': row[0], 'lat': row[1], 'lon': row[2], 'id': row[3]})
	conn.close()
	return locs

def get_records(loc_id):
	conn=sqlite3.connect(db_file)
	c=conn.cursor()
	c.row_factory = sqlite3.Row
	c.execute("SELECT day, air_temp, ground_temp, soil_moisture, precip, snow_depth, snow_fall, albedo FROM measurement WHERE loc_id=%d ORDER BY day" % loc_id)

	dates=[]
	data={'air_temp': [], 'ground_temp': [], 'soil_moisture':[], 'precip':[], 'snow_depth': [], 'snow_fall':[], 'albedo':[]}
	for row in c:
		d=datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
		d=d.replace(tzinfo=tz.gettz('UTC'))
		dates.append(d)
		for key in data.keys():
			data[key].append(row[key])
	conn.commit()
	conn.close()
	return (dates, data)

def add_location(name, lat, lon, elev):
	conn=sqlite3.connect(db_file)
	c=conn.cursor()
	c.execute("INSERT INTO location(name, lat, lon, elevation) VALUES('%s', %f, %f, %f)" % (name, lat, lon, elev))
	conn.commit()
	conn.close()	

def add_record(loc_id, dt, air, ground, soil_moisture):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	c.execute("""INSERT INTO measurement (loc_id,
	day,
	air_temp,
	ground_temp,
	soil_moisture)
	 VALUES (%d, datetime('%s'), %f, %f, %f)"""
	% (loc_id, dt.strftime("%Y-%m-%d %H:00"), air, ground, soil_moisture))
	conn.commit()
	conn.close()

