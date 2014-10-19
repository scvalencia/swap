from django.conf.urls import patterns, include, url

from .views import HomeView, UserZoneView


genericusers_urls = patterns('',
	url(r'^$', HomeView.as_view()),
    url(r'^userzone/', UserZoneView.as_view()),
)