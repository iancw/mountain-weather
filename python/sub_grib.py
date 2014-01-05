import pygrib
import os
import os.path

def create_sub(full_grib, data_dir='.'):
  ''' Extracts a subset of GRIB records from full_grib and 
  saves them in a file named the same as full_grib, but in 
  the data_dir folder.
  '''
  #names=['Temperature', 'Soil temperature', 'Total precipitation', 'Wind speed (gust)', 'Water equivalent of accumulated snow depth']
  name, ext = os.path.splitext(full_grib)
  out_file = '{2}/{0}_sub{1}'.format(name, ext, data_dir)
  grbout = open(out_file, 'wb')

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
  return out_file
