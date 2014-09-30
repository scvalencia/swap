from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^login/', views.login, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^home/', views.home, name='home'),
)