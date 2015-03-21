from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from FMS import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FMS_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^FMS/', include('FMS.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^search/$', views.search, name='search_for_something'),

    )
    
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^media/(?P<path>.*)',
    'serve',
    {'document_root': settings.MEDIA_ROOT}), )
