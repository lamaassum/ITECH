from django.conf.urls import patterns, url, include
from FMS import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    #url(r'^ajax_search/', include('ajax_search.urls')),
    url(r'^my_profile/$', views.my_profile, name='my_profile'))

