import pygrib
import numpy as np

def find_index(lat, lon, grb):
	#lats and lons will have the same shape as data
	lats,lons = grb.latlons()
	#old rag: 38.551968°, -78.314666°
	lat=38.551968
	lon= -78.314666
	idx=((lats-lat)**2 + (lons-lon)**2).argmin()
	np.unravel_index(idx, data.shape)

def open(file):
	grbs=pygrib.open(file)
	grb=grbs.select(typeOfLevel='surface',name='Temperature')[0]
	data=grb.values
	