from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

import bs4
import json
import requests


class NewsCrawl(object):
    """
    Class used for making news requests.
    """
    URL_BASE = 'https://www.google.com/search'

    def __init__(self):
        self.payload = {
            'tbm': 'nws',
        }
        self.url = self.URL_BASE

    def crawl_term(self, q):
        if not q:
            return json.dumps([])
        self.payload['q'] = q
        r = requests.get(self.url, params=self.payload)
        html = r.text
        soup = bs4.BeautifulSoup(html)
        titles = soup.find_all('a')
        ans = []
        for t in titles:
            text = t.text
            href = t.get('href').split('=')
            if text.lower().find(q) != -1:
                if len(href) > 1:
                    data = {
                        'title': text,
                        'url': href[1],
                    }
                    ans.append(data)
        return json.dumps(ans)


class NewsView(View):
    """
    The view endpoint of the news api.
    """
    def get(self, request, *args, **kwargs):
        news_crawl = NewsCrawl()
        news = news_crawl.crawl_term(request.GET.get('q'))
        return HttpResponse(news, content_type='application/json')