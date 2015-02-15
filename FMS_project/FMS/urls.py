from django.conf.urls import patterns, url
from FMS import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'))
