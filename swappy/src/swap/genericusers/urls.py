from django.conf.urls import patterns, include, url


genericusers_urls = patterns('',
    # Examples:
    # url(r'^$', 'swap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^userzone/', 'genericusers.views.userzone', name='userzone'),
)