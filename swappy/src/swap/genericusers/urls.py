from django.conf.urls import patterns, include, url

from .views import UserzoneView


genericusers_urls = patterns('',
    url(r'^userzone/', UserzoneView.as_view()),
)