from django.conf.urls import patterns, url, include
from FMS import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    #url(r'^ajax_search/', include('ajax_search.urls')),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^profile_form/$', views.profile_form, name='profile_form'),
    url(r'^(?P<user_name_slug>[\w\-]+)/$', views.profile, name='profile'),
    )


