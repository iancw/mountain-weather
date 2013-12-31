import pygrib
import os
import os.path

def create_sub(full_grib, data_dir='.'):
  #names=['Temperature', 'Soil temperature', 'Total precipitation', 'Wind speed (gust)', 'Water equivalent of accumulated snow depth']
  name, ext = os.path.splitext(full_grib)
  grbout = open('{2}/{0}_sub.{1}'.format(name, ext, data_dir), 'wb')

  grbs = pygrib.open(full_grib)
  surface_names=['t', 'acpcp', 'gust', 'sdwe']
  for name in surface_names:
    print 'finding {0}'.format(name)
    grbs.seek(0)
    for grb in grbs.select(shortName=name, typeOfLevel='surface'):
      grbout.write(grb.tostring())
  agl_names=['10u', '10v']
  grbs.seek(0)
  for name in agl_names:
    print 'finding {0}'.format(name)
    for grb in grbs.select(shortName=name, typeOfLevel='heightAboveGround'):
      grbout.write(grb.tostring())

  grbout.close()
