from django.conf.urls import patterns, include, url
from django.contrib import admin

from genericusers.urls import userpatterns

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^solicitudes/', include('solicitudes.urls')),
    url(r'^swaptransactions/', include('swaptransactions.urls')),
    url(r'^vals/', include('vals.urls')),
)

urlpatterns += userpatterns