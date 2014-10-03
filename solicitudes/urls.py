from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^new_solicitude/$', views.new_solicitude, name='new_solicitude'),
    url(r'^active_solicitudes/$', views.active_solicitudes, name='active_solicitudes'),
    url(r'^passive_pending_solicitudes/$', views.passive_pending_solicitudes, name='passive_pending_solicitudes'),
    url(r'^passive_solicitudes/$', views.passive_solicitudes, name='passive_solicitudes'),
    url(r'^(\d+)/$', views.solicitude, name='solicitude')
)