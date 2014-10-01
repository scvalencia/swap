from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('genericusers.urls')),
    url(r'^solicitudes/', include('solicitudes.urls')),
    url(r'^swaptransactions/', include('swaptransactions.urls')),
    url(r'^vals/', include('vals.urls')),
)
