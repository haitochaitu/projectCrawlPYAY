from django.conf.urls import url
from appCrawl.api.api import Crawl

urlpatterns = [
    url(r'^pageCrawl/$', 'appCrawl.views.pageCrawl'),
    url(r'^pageResult/$', 'appCrawl.views.pageResult'),
    url(r'^crawlfromurlapi/$', Crawl.as_view()),
]