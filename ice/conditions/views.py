from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from conditions.models import Location, Measurement

def index(request):
	locations = Location.objects.all()
	context = {'locations': locations}
	return render(request, 'index.html', context)

def detail(request, location_id):
	location = Location.objects.get(pk=location_id)
	meas = Measurement.objects.filter(location=location)
	context = {'location': location, 'measurements': meas}
	return render(request, 'location.html', context)