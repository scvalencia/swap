from django.conf.urls import patterns, include, url

from .views import NewsView


news_urls = patterns('',
    url(r'^news', NewsView.as_view()),
)