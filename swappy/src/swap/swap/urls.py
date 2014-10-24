from django.conf.urls import patterns, include, url
from django.contrib import admin

from genericusers.urls import genericusers_urls
from news.urls import news_urls


urlpatterns = patterns('')

urlpatterns += genericusers_urls
urlpatterns += news_urls