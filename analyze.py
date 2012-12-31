import pygrib
import numpy as np
from mpl_toolkits.basemap import Basemap, cm
# requires netcdf4-python (netcdf4-python.googlecode.com)
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt

def find_index(lat, lon, grb):
	#lats and lons will have the same shape as data
	lats,lons = grb.latlons()
	idx=((lats-lat)**2 + (lons-lon)**2).argmin()
	return np.unravel_index(idx, lats.shape)

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

def mark_loc(grb, m, lat=38.551968, lon=-78.314666):
	poly = m.tissot(lon,lat,0.02,100,facecolor='green',zorder=10,alpha=0.5)
	(x,y)=find_index(lat, lon, grb)
	lats,lons=grb.latlons()
	points=[(lats[x,y], lons[x,y]), (lats[x+1,y], lons[x+1,y]), (lats[x,y+1],lons[x,y+1]),\
	(lats[x+1,y+1], lons[x+1,y+1]), (lats[x-1,y-1], lons[x-1,y-1]),(lats[x,y-1], lons[x,y-1])]
	for point in points:
		poly = m.tissot(point[1],point[0],0.01,100,facecolor='green',zorder=10,alpha=0.5)
