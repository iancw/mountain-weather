from models import Location, Measurement

import pygrib
from datetime import *
import numpy as np
from dateutil import tz
from django.utils.timezone import utc
import re

def populate_dc_locs():
	l=Location(name='Overall Falls', lat=38.783360, lon=-78.295143)
	l.save()
	l=Location(name='Lewis Spring Falls', lat=38.520638, lon=-78.450539)
	l.save()
	l=Location(name='White oak canyon', lat=38.555984, lon=-78.353889)
	l.save()
	l=Location(name='Finleys Folly', lat=37.911125, lon=-78.973633)
	l.save()

def parse_dt(filename):
	m=re.match(r'.*(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})_(\d{3}).grb$', filename)
	dt=datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
	dt=dt+timedelta(hours=int(m.group(6)))
	return dt.replace(tzinfo=utc)

def parse_tau(filename):
	m=re.match(r'.*(\d{4})(\d{2})(\d{2})_(\d{4})_(\d{3}).grb$', filename)
	return int(m.group(5))

#glob.glob('data/*.grb'):
def populate(files):
	for filename in files:
		print "Processing %s" % filename
		tau=parse_tau(filename)
		dt=parse_dt(filename)
		should_process=True
		print "Looking for other measurements at {0}".format( dt )
		for m in Measurement.objects.filter(date=dt):
			print "Found measurement at {0} with tau {1}".format( m.date, m.tau )
			should_process=False
			#Process the new file if any of the old measurements at that date
			# have a larger tau (if they are further from a base time)
			if tau < m.tau:
				should_process = True
				break
		if should_process:
			for m in Measurement.objects.filter(date=dt):
				m.delete()
			try:
				process(filename)
			except ValueError as e:
				print "Could not process {0}".format(filename)
				print(e)
		else:
			print "Data for  %s is already up to date" % filename

def process(grb_file):
	locs = Location.objects.all()
	grbs=pygrib.open(grb_file)

	variables=[('Temperature', 'surface', 'air_temp'), 
	('Soil Temperature', 'depthBelowLand', 'ground_temp'),
	('Soil Moisture', 'depthBelowLandLayer', 'soil_moisture'),
	('Total Precipitation', 'surface', 'precip'),
	('Snow depth water equivalent', 'surface', 'snow_depth'),
	('Snow Fall water equivalent', 'surface', 'snow_fall'),
	('Albedo', 'surface', 'albedo'),
	('Orography', 'surface', 'orography')
	]
	dt = find_date(grbs.select(typeOfLevel='surface',name='Temperature')[0])
	loc_data={}
	for loc in locs:
		loc_data[loc] = {}

	for v in variables:
		print "processing {0}".format( v[0] )
		ld=process_var(grbs.select(typeOfLevel=v[1],name=v[0])[0], locs)
		for loc in locs:
			loc_data[loc][v[2]] = ld[loc]

	print loc_data
	for loc in locs:
		data_dic={}
		for v in variables:
			data_dic[v[2]] = loc_data[loc][v[2]]
		data_dic['date']=dt
		data_dic['location']=loc
		data_dic['tau']=parse_tau(grb_file)
		print data_dic
		m=Measurement(**data_dic)
		m.save()

def process_var(temp, locs):
	data=temp.values
	loc_data={}
	for loc in locs:
		idx=find_index(loc.lat, loc.lon, temp)
		t=data[idx[0], idx[1]]
		print "%s at %s is %f" % (temp.name, loc.name, t)
		loc_data[loc]=t
	return loc_data

def find_date(grb):
	dt= datetime.strptime("%d%02d" % (grb.dataDate, grb.dataTime), "%Y%m%d%H%M") + timedelta(hours=grb.startStep)
	return dt.replace(tzinfo=utc)

def find_index(lat, lon, grb):
	#lats and lons will have the same shape as data
	lats,lons = grb.latlons()
	idx=((lats-lat)**2 + (lons-lon)**2).argmin()
	return np.unravel_index(idx, lats.shape)
