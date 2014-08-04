from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from pari.news.views import PariNewsView, NewsPostList, NewsPostDetail, LatestArticleList

urlpatterns = patterns('pari.news.views',
                       url(r'^latest-articles/$', LatestArticleList.as_view(), name='latest-articles'),
                       url(r'^news/(?P<slug>.+)/$', NewsPostDetail.as_view(), name='news-detail'),
                       url(r'^news/$', NewsPostList.as_view(), name='news-list'),
                       url(r'^$', PariNewsView.as_view(), name='pari-news'))

urlpatterns += staticfiles_urlpatterns()
