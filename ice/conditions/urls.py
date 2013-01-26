from django.conf.urls import patterns, url

from conditions import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^location/(?P<location_id>\d+)/$', views.detail, name='detail'),
)