from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from grib import Grib
import numpy as np

def plot(rec):
  data = rec.values
  lats, lons = rec.latlons()
  fig = plt.figure(figsize=(8,8))
  # create figure and axes instances
  ax = fig.add_axes([0.1,0.1,0.8,0.8])
  # create polar stereographic Basemap instance.
#  m = Basemap(projection='stere',lon_0=lon_0,lat_0=90.,lat_ts=lat_0,\
#    llcrnrlat=latcorners[0],urcrnrlat=latcorners[2],\
#    llcrnrlon=loncorners[0],urcrnrlon=loncorners[2],\
#    rsphere=6371200.,resolution='l',area_thresh=10000)
#
  # Lambert Conformal Conic map.
  m = Basemap(llcrnrlon=-100.,llcrnrlat=0.,urcrnrlon=-20.,urcrnrlat=57.,
    projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,
    resolution ='l',area_thresh=1000.)

  # draw coastlines, state and country boundaries, edge of map.
  m.drawcoastlines()
  m.drawstates()
  m.drawcountries()
  # draw parallels.
  parallels = np.arange(0.,90,10.)
  m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
  # draw meridians
  meridians = np.arange(180.,360.,10.)
  m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

  ny = data.shape[0]; nx = data.shape[1]

  x, y = m(lons, lats) # compute map proj coordinates.
  m.contourf(x, y, data)
  plt.title('{0} ({5}) for period ending {1}/{2}/{3} {4}:00'.format(rec.parameterName, rec.year, rec.month, rec.day, rec.hour, rec.parameterNumber))
  plt.show()
