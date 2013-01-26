from django.db import models

# Create your models here.

class Location(models.Model):
	name = models.CharField(max_length=100)
	lat = models.FloatField()
	lon = models.FloatField()

	class Meta:
		unique_together = ('lat', 'lon')

	def __unicode__(self):
		return self.name

class Measurement(models.Model):
	date = models.DateTimeField()
	air_temp = models.FloatField()
	ground_temp = models.FloatField()
	soil_moisture = models.FloatField()
	precip = models.FloatField()
	snow_depth = models.FloatField()
	snow_fall = models.FloatField()
	albedo = models.FloatField()
	orography = models.FloatField()
	location = models.ForeignKey(Location)
	tau = models.IntegerField()
	
	class Meta:
		unique_together = ('date', 'location')