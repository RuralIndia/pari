from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from pari.news.views import NewsPostList, NewsPostDetail, LatestArticleList

urlpatterns = patterns('pari.news.views',
                       url(r'^latest-articles/$', LatestArticleList.as_view(), name='latest-articles'),
                       url(r'^(?P<slug>.+)/$', NewsPostDetail.as_view(), name='news-detail'),
                       url(r'^$', NewsPostList.as_view(), name='news-list'))

urlpatterns += staticfiles_urlpatterns()
