from django.conf.urls import patterns, include, url

from .views import AdminView, HomeView, UserZoneView, APIView, LogoutView


genericusers_urls = patterns('',
	url(r'^$', HomeView.as_view()),
	url(r'^admin/$', AdminView.as_view()),
	url(r'^admin/api/$', AdminView.as_view()),
	url(r'^admin/$', AdminView.as_view()),
    url(r'^userzone/$', UserZoneView.as_view()),
    url(r'^api/(?P<param>\w+)/$', APIView.as_view()),
    url(r'^logout/$', LogoutView.as_view())
)