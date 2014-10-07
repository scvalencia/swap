from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^active_transactions/$', views.active_transactions, name='active_transactions'),
)