import urllib2
from datetime import *

#201212/20121229/nam_218_20121229_0000_000.grb
def make_nomads_suffix(dt):
	daymoyr = dt.strftime('%Y%m%d')
	#base='0000' #0, 6, 12, 18.  four digits zero padded
	base=(dt.hour // 6) * 6 # Use integer division to find nearest base time...
	#tau='000' #3 hour intervals, three digits zero padded
	tau=((dt.hour - base) // 3) * 3
	return '{0}/{1}/nam_218_{1}_{2}_{3}.grb'.format(dt.strftime('%Y%m'), daymoyr, '%02d00' % base, '%03d' % tau)

def download(dt):
	#http://nomads.ncdc.noaa.gov/data/meso-eta-hi/201212/20121229/nam_218_20121229_0000_000.grb
	nomads_prefix='http://nomads.ncdc.noaa.gov/data/meso-eta-hi/'
	#201212/20121229/nam_218_20121229_0000_000.grb')
	date_suffix=make_nomads_suffix(dt)
	print 'Opening {0}...'.format(nomads_prefix + date_suffix)
	u = urllib2.urlopen(nomads_prefix + date_suffix)
	localFile = open('temp.grib', 'w')
	print 'Reading {0}...'.format(nomads_prefix + date_suffix)
	st=datetime.now()
	localFile.write(u.read())
	en=datetime.now()
	localFile.close()
	print 'Downloaded in %.2f seconds' % (en-st).total_seconds()
