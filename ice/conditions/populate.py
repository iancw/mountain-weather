from models import Location, Measurement

import pygrib
from datetime import *
import numpy as np
from dateutil import tz

def populate_dc_locs():
	l=Location(name='Overall Falls', lat=38.783360, lon=-78.295143)
	l.save()
	l=Location(name='Lewis Spring Falls', lat=38.520638, lon=-78.450539)
	l.save()
	l=Location(name='White oak canyon', lat=38.555984, lon=-78.353889)
	l.save()
	l=Location(name='Finleys Folly', lat=37.911125, lon=-78.973633)
	l.save()
#glob.glob('data/*.grb'):
def populate(files):
	print "Processing %s" % f
	process(f)

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
	return datetime.strptime("%d%02d" % (grb.dataDate, grb.dataTime), "%Y%m%d%H%M") + timedelta(hours=grb.startStep)

def find_index(lat, lon, grb):
	#lats and lons will have the same shape as data
	lats,lons = grb.latlons()
	idx=((lats-lat)**2 + (lons-lon)**2).argmin()
	return np.unravel_index(idx, lats.shape)
