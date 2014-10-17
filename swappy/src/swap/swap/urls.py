from django.conf.urls import patterns, include, url
from django.contrib import admin

from genericusers.urls import genericusers_urls
from home.urls import home_urls
from news.urls import news_urls


urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += genericusers_urls
urlpatterns += home_urls
urlpatterns += news_urls