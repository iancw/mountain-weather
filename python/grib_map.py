
short_names=['t', 'acpcp', 'gust', 'sdwe']
agl_names=['10u', '10v']

def get_hrrr_params():
  params=[]
  for name in surface_names:
    params.append((name, 'surface'))
  for name in agl_names:
    params.append((name, 'heightAboveGround'))

def get_rap_params():
  params=[]
  for name in surface_names:
    params.append((name, 'surface'))
  for name in agl_names:
    params.append((name, 'heightAboveGround'))
