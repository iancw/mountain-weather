import urllib2
from datetime import *
import os.path

#201212/20121229/nam_218_20121229_0000_000.grb
def make_nomads_suffix_dt(dt):
	base=(dt.hour // 6) * 6 # Use integer division to find nearest base time...
	tau=((dt.hour - base) // 3) * 3
	return make_nomads_suffix(dt, base, tau)
	
#base='0000' #0, 6, 12, 18.  four digits zero padded
#tau='000' #3 hour intervals, three digits zero padded
def make_nomads_suffix(dt, base, tau):
	daymoyr = dt.strftime('%Y%m%d')
	return '{0}/{1}/nam_218_{1}_{2}_{3}.grb'.format(dt.strftime('%Y%m'), daymoyr, '%02d00' % base, '%03d' % tau)

def make_local_name(dt):
	return '{0}.grb'.format(dt.strftime('%Y%m%d%H'))

def download_history():
	#just jan for now...
	n=datetime.now()
	for d in range(1, n.day):
		for h in xrange(0, 23, 3):
			download(datetime(n.year, n.month, d, h))


#Downloads all gribs from the previous days 18 base time out
# to tau 84 at 3 hour steps
def download_forecasts():
	d=datetime.now()#-timedelta(days=1)
	#
	for t in xrange(0, 84, 3):
		download_suffix(make_nomads_suffix(d, 6, t))

def download(dt):
	date_suffix=make_nomads_suffix_dt(dt)
	download_suffix(date_suffix)

def download_suffix(date_suffix):
	#http://nomads.ncdc.noaa.gov/data/meso-eta-hi/201212/20121229/nam_218_20121229_0000_000.grb
	nomads_prefix='http://nomads.ncdc.noaa.gov/data/meso-eta-hi/'
	#201212/20121229/nam_218_20121229_0000_000.grb')
	print 'Opening {0}...'.format(nomads_prefix + date_suffix)
	u = urllib2.urlopen(nomads_prefix + date_suffix)
	fname = 'data/'+os.path.basename(date_suffix)
	if os.path.isfile(fname):
		print 'File {0} already exists'.format(fname)
		return
	localFile = open(fname, 'w')
	print 'Reading {0}...'.format(nomads_prefix + date_suffix)
	st=datetime.now()
	localFile.write(u.read())
	en=datetime.now()
	localFile.close()
	print 'Downloaded in %.2f seconds' % (en-st).total_seconds()
