from django.conf.urls import patterns, include, url

import views


userpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),
)