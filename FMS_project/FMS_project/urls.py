from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from FMS import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FMS_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login',{"template_name" : "registration/login.html",},name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{"template_name" : "registration/logout.html",},name="logout"),
    url(r'^$', views.index, name='index'),
    url(r'^advanced_search/$', views.issues_search, name='advanced_student_search_form'),
    url(r'^results/$', views.advanced_search, name='advanced_search'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^profile_form/$', views.profile_form, name='profile_form'),
    url(r'^favorite_supervisor/$', views.favorite_supervisor, name='favorite_supervisor'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', views.about, name='about'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^/$', views.search, name='search_for_something'),
    url(r'^(?P<user_name_slug>[\w\-]+)/$', views.profile, name='profile'),
    )
    
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^media/(?P<path>.*)',
    'serve',
    {'document_root': settings.MEDIA_ROOT}), )
