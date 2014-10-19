from django.conf.urls import patterns, include, url
from django.contrib import admin

from actives.urls import actives_urls
from genericusers.urls import genericusers_urls
from news.urls import news_urls
from vals.urls import vals_urls


urlpatterns = patterns('')

urlpatterns += actives_urls
urlpatterns += genericusers_urls
urlpatterns += news_urls
urlpatterns += vals_urls