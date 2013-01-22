import pygrib
from numpy import genfromtxt
import numpy as np
from datetime import *

class nam_grib:
	"""
	Wraps pygrib and uses the grib inventory file to interpret it based on parameter numbers
	"""

	def __init__(self, file):
		self.gribs = pygrib.open(file)
		self.inv = self.read_inv()

	def read_inv(self):
		inv=[]
		lines=open('nam.inv').read().splitlines()
		for line in lines:
			#param id: offset : date : short name : level : kpds : anl : bad desc : good desc
			vals=line.split(':')
			inv.append({'paramId':int(vals[0]), 'shortName': vals[3], 'level':vals[4], 'desc':vals[-1] })
		return np.array(inv)

	def test(self):
		variables=[('Temperature', 'surface', 'air_temp'), 
		('Soil Temperature', 'depthBelowLand', 'ground_temp'), 
		('Soil Moisture', 'depthBelowLandLayer', 'soil_moisture'),
		('Total Precipitation', 'surface', 'precip'),
		('Snow depth water equivalent', 'surface', 'snow_depth'),
		('Snow Fall water equivalent', 'surface', 'snow_fall'),
		('Albedo', 'surface', 'albedo'),
		('Orography', 'surface', 'orography'),
		('Ice cover', 'surface', 'ice_cover')]
		
		for var in variables:
			msg=self.gribs.select(typeOfLevel=var[1], name=var[0])[0]
			print msg
			inv=self.find_inv(msg)
			print inv
		
	def find_date(self, grb):
		return datetime.strptime("%d%02d" % (grb.dataDate, grb.dataTime), "%Y%m%d%H%M") + timedelta(hours=grb.startStep)

	def find_inv(self, msg):
		"""
		Finds an inventory dictionary for a given pygrib message
		"""
		for dic in self.inv:
			if dic['paramId'] == msg.messagenumber:
				dic['date']=self.find_date(msg)
				return dic
		return {'paramId': msg.messagenumber, 'date':self.find_date(msg), 'shortName':msg.shortName, 'level':msg.typeOfLevel, 'desc':msg.parameterName}

	def get_inv(self):
		inventory=[]
		for g in self.gribs:
			inv=self.find_inv(g)
			inventory.append(inv)
		return inventory

	def print_inventory(self):
		for inv in self.get_inv():
			print inv

	def __repr__(self):
		inventory=[]
		for inv in self.get_inv():
			inventory.append(repr(inv['paramId']))
			inventory.append(repr(inv['date']))
			inventory.append(repr(inv['shortName']))
			inventory.append(repr(inv['level']))
			inventory.append(repr(inv['desc']))
		return ':'.join(inventory)
