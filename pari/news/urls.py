from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pari.news.views import LatestArticleList

urlpatterns = patterns('pari.news.views', url(r'^latest-articles/$', LatestArticleList.as_view(), name='latest-articles'))

urlpatterns += staticfiles_urlpatterns()
