from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^$', views.signup, name='signup'),
)
