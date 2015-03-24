from django.conf.urls import patterns, url, include
from FMS import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^advanced_search/$', views.issues_search, name='advanced_student_search_form'),
    url(r'^results/$', views.advanced_search, name='advanced_search'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^profile_form/$', views.profile_form, name='profile_form'),
    url(r'^(?P<user_name_slug>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^favorite_supervisor/$', views.favorite_supervisor, name='favorite_supervisor'),
    )
