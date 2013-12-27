from models import Location, Measurement

import numpy as np
from datetime import *
from dateutil import tz
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import matplotlib
from matplotlib.dates import DateFormatter
import matplotlib.dates
from django.utils.timezone import utc

def kelvin_to_fahr(l):
	return ((np.array(l) - 273.15) * 1.8) + 32.0

def to_local(dates):
	local=tz.gettz('America/New_York')
	return [d.replace(tzinfo=utc).astimezone(local) for d in dates]

def now_local():
	dt=datetime.now()
	return dt.replace(tzinfo=utc).astimezone(tz.gettz('America/New_York'))

def plot_all(loc_name):
	locs=Location.objects.filter(name=loc_name)
	for loc in locs:
		plot_loc(loc)

def plot_loc(loc):
	temps=[]
	dates=[]
	albedo=[]
	local_tz=tz.gettz('America/New_York')
	for m in Measurement.objects.filter(location=loc):
		temps.append(m.air_temp)
		dates.append(m.date)
		albedo.append(m.albedo)
	air_f = kelvin_to_fahr(temps)
	plot_dates = matplotlib.dates.date2num(to_local(dates))
	plot_now = matplotlib.dates.date2num(datetime.now())
	fig=plt.figure()
	ax=fig.add_subplot(111)
	ax.plot_date(plot_dates, air_f, '-', label='air_temp')
	ax.fmt_xdata = DateFormatter('%a %b %d %H:%M', tz=local_tz)
	ax.xaxis.set_major_formatter(DateFormatter('%a %b %d %H:%M', tz=local_tz))
	ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(tz=local_tz))
	#ax.axvline(x=plot_now)
	ax.axvline(x=datetime(2013, 1, 22, 0).replace(tzinfo=local_tz))
	ax.axvline(x=datetime(2013, 1, 23, 0).replace(tzinfo=local_tz))
	ax.axvline(x=datetime(2013, 1, 24, 0).replace(tzinfo=local_tz))
	ax.axvline(x=datetime(2013, 1, 25, 0).replace(tzinfo=local_tz))
	ax.axhline(y=20)
	ax.legend()

	#ax2=ax.twinx()
	#ax2.plot_date(plot_dates, albedo, '-g', label='albedo')
	#ax2.legend()

	plt.title(loc.name)
	plt.show()