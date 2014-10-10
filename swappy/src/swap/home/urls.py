from django.conf.urls import patterns, include, url


home_urls = patterns('',
    # Examples:
    # url(r'^$', 'swap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'home.views.home', name='home'),
)