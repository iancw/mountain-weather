from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from conditions.models import Location

def index(request):
	locations = Location.objects.all()
	context = {'locations': locations}
	return render(request, 'index.html', context)