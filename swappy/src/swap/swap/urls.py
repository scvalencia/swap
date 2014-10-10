from django.conf.urls import patterns, include, url
from django.contrib import admin

from genericusers.urls import genericusers_urls
from home.urls import home_urls


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'swap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += genericusers_urls
urlpatterns += home_urls