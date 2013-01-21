import pygrib
import numpy as np
from mpl_toolkits.basemap import Basemap, cm
# requires netcdf4-python (netcdf4-python.googlecode.com)
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import database
from datetime import *
import glob

def process_all():
	for f in glob.glob('*.grb'):
		print "Processing %s" % f
		process(f)

def process(grb_file):
	locs=database.get_locs()
	grbs=pygrib.open(grb_file)

	variables=[('Temperature', 'surface', 'air_temp'), 
	('Soil Temperature', 'depthBelowLand', 'ground_temp'), 
	('Soil Moisture', 'depthBelowLandLayer', 'soil_moisture')]
	dt=datetime.now()
	for v in variables:
		dt=process_var(grbs.select(typeOfLevel=v[1],name=v[0])[0], locs, v[2])

	for loc in locs:
		database.add_record(loc['id'], dt, loc['air_temp'], loc['ground_temp'], loc['soil_moisture'])

def plot_all():
	(dates, air, ground, moist)=database.get_records(0)


def process_var(temp, locs, key):
	dt = find_date(temp)
	data=temp.values
	for loc in locs:
		idx=find_index(loc['lat'], loc['lon'], temp)
		t=data[idx[0], idx[1]]
		print "%s at %s is %f" % (key, loc['name'], t)
		loc[key]=t
	return dt
		
def find_date(grb):
	return datetime.strptime("%d%d" % (grb.dataDate, grb.dataTime), "%Y%m%d%H%M")

def find_index(lat, lon, grb):
	#lats and lons will have the same shape as data
	lats,lons = grb.latlons()
	idx=((lats-lat)**2 + (lons-lon)**2).argmin()
	return np.unravel_index(idx, lats.shape)

# Other surface variables...
# Total Precipitation, Convective precipitation (water), Snow Fall water equivalent, Snow depth water equivalent, Ice cover
# Soil Temperature layer:  depthBelowLand
# Soil Moisture:  depthBelowLandLayer
# Orography
def open(file):
	grbs=pygrib.open(file)
	grb=grbs.select(typeOfLevel='surface',name='Temperature')[0]
	data=grb.values
	lat=38.551968
	lon= -78.314666
	idx=find_index(lat, lon, grb)
	print data[idx[0], idx[1]]

def make_basemap(grb):
	p=grb.projparams
	lats,lons=grb.latlons()
	m=Basemap(projection='lcc',lon_0=p['lon_0'],lat_0=p['lat_0'],lat_1=p['lat_1'],\
		resolution='i',\
		llcrnrlat=lats[0,0],urcrnrlat=lats[-1,-1],\
		llcrnrlon=lons[0,0],urcrnrlon=lons[-1,-1],\
		rsphere=(p['a'],p['b']))
	m.imshow(grb.values)
	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()
	return m

def save_var(grb, var):
	print var+'.nc'
	d = Dataset(var+'.nc', 'w')
	d.createDimension('x')
	d.createDimension('y')
	lats, lons = grb.latlons()
	nc_var = d.createVariable(var, 'f4', ('x', 'y'))
	nc_var[:] = grb.values
	lat_var = d.createVariable('lats', 'f4', ('x', 'y'))
	lat_var[:] = lats
	lon_var = d.createVariable('lons', 'f4', ('x', 'y'))
	lon_var[:] = lons
	d.close()


def mark_loc(grb, m, lat=38.551968, lon=-78.314666):
	poly = m.tissot(lon,lat,0.02,100,facecolor='green',zorder=10,alpha=0.5)
	(x,y)=find_index(lat, lon, grb)
	lats,lons=grb.latlons()
	points=[(lats[x,y], lons[x,y]), (lats[x+1,y], lons[x+1,y]), (lats[x,y+1],lons[x,y+1]),\
	(lats[x+1,y+1], lons[x+1,y+1]), (lats[x-1,y-1], lons[x-1,y-1]),(lats[x,y-1], lons[x,y-1])]
	for point in points:
		poly = m.tissot(point[1],point[0],0.01,100,facecolor='green',zorder=10,alpha=0.5)
