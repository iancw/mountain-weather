import urllib2
from datetime import *
import os.path
import os
import glob
import re

#http://nomads.ncdc.noaa.gov/data/meso-eta-hi/201212/20121229/nam_218_20121229_0000_000.grb
nomads_prefix='http://nomads.ncdc.noaa.gov/data/meso-eta-hi/'

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
	beg=datetime(2013, 1, 1, 0)
	n=datetime.now()
	try:
		while (beg < n):
			download(datetime(beg.year, beg.month, beg.day, beg.hour))
			beg = beg + timedelta(hours=3)
	except:
		pass

def update():
	download_history()
	remove_old_forecasts()
	download_forecasts()

def find_most_recent_base():
	for dt in [datetime.now(), datetime.now()-timedelta(days=1), datetime.now()-timedelta(days=2), datetime.now()-timedelta(days=3), datetime.now()-timedelta(days=4)]:
		for base in [18, 12, 6, 0]:
			for t in range(0, 6):
				date_suffix=make_nomads_suffix(dt, base, t)
				try:
					print 'trying ...{0}{1}...'.format(nomads_prefix,  date_suffix)
					u = urllib2.urlopen('{0}{1}'.format(nomads_prefix, date_suffix))
					return datetime(dt.year, dt.month, dt.day, base, t)
				except:
					pass
	raise StandardError('Could not find a recent base')

def parse_tau(filename):
	m=re.match(r'.*(\d{4})(\d{2})(\d{2})_(\d{4})_(\d{3}).*', filename)
	return int(m.group(5))

# Old forecasts have taus from 6 on up
def remove_old_forecasts():
	for f in glob.glob('data/*.grb'):
		if parse_tau(f) > 3:
			print "deleting {0}".format(f)
			os.remove(f)

#Downloads all gribs from the previous days 18 base time out
# to tau 84 at 3 hour steps
def download_forecasts():
	d=find_most_recent_base()
	for t in xrange(0, 85, 1):
		suf=make_nomads_suffix(d, d.hour, t)
		try:
			download_suffix(suf)
		except:
			print 'problems downloading {0}'.format(suf)

def download(dt):
	date_suffix=make_nomads_suffix_dt(dt)
	download_suffix(date_suffix)

def download_suffix(date_suffix):
	#201212/20121229/nam_218_20121229_0000_000.grb')
	fname = 'data/'+os.path.basename(date_suffix)
	u = urllib2.urlopen(nomads_prefix + date_suffix)
	if os.path.isfile(fname):
		return
	print 'Opening {0}...'.format(nomads_prefix + date_suffix)
	localFile = open(fname, 'w')
	print 'Reading {0}...'.format(nomads_prefix + date_suffix)
	st=datetime.now()
	localFile.write(u.read())
	en=datetime.now()
	localFile.close()
	print 'Downloaded in %.2f seconds' % (en-st).total_seconds()
