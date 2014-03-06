
def kelv_to_fahr(k):
  return ((k - 273.15) * 1.8) + 32.0

def mps_to_mph(ms):
  return 2.23694 * ms

# From http://www.slf.ch/info/mitarbeitende/marty/publications/Jonas2009_EstimatingSWE.pdf
# Using median value for pb...
# swe is snow water equivalent in kgm-3
def swe_to_in(swe):
  pb = 300.0
  hs_m = swe / pb
  return hs_m * 39.3701



