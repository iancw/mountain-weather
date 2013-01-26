from django import template

register = template.Library()

def to_fahrenheit(k):
	return ((k - 273.15) * 1.8) + 32.0

register.filter('to_fahrenheit', to_fahrenheit)