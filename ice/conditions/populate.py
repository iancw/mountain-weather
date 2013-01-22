from models import Location

def populate_dc_locs():
	l=Location(name='Overall Falls', lat=38.783360, lon=-78.295143)
	l.save()
	l=Location(name='Lewis Spring Falls', lat=38.520638, lon=-78.450539)
	l.save()
	l=Location(name='White oak canyon', lat=38.555984, lon=-78.353889)
	l.save()
	l=Location(name='Finleys Folly', lat=37.911125, lon=-78.973633)
	l.save()