from django.conf.urls import patterns, include, url

from .views import HomeView


home_urls = patterns('',
    # Examples:
    # url(r'^$', 'swap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomeView.as_view()),
)