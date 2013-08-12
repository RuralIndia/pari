from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (LocationListApi, LocationDetailApi, LocationArticleApi,
                    LocationDetail, CategoriesList, CategoryDetail, ArticleDetail,
                    KeywordDetail, AuthorDetail, ArchiveDetail)

root_patterns = patterns('pari.article.views',
    url(r'^categories/(?P<slug>.+)/$', CategoryDetail.as_view(), name='category-detail'),
    url(r'^categories/$', CategoriesList.as_view(), name='category-list'),
    url(r'^authors/(?P<slug>.+)/$', AuthorDetail.as_view(), name='author-detail'),
    url(r'^articles/(?P<slug>.+)/$', ArticleDetail.as_view(), name='article-detail'),
    url(r'^topics/(?P<slug>.+)/$', ArticleDetail.as_view(), name='topic-detail'),
    url(r'^locations/(?P<slug>.+)/$', LocationDetail.as_view(), name='location-detail'),
    url(r'^keywords/(?P<slug>.+)/$', KeywordDetail.as_view(template_name="article/keyword_detail.html"), name='keyword-detail'),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d+)/$', ArchiveDetail.as_view(), name='archive-detail'),
)


urlpatterns = patterns('pari.article.views',
    url(r'^api/$', 'api_root'),
    url(r'^api/locations/$', LocationListApi.as_view(), name='api-location-list'),
    url(r'^api/locations/(?P<pk>\d+)/$', LocationDetailApi.as_view(), name='api-location-detail'),
    url(r'^api/locations/(?P<pk>\d+)/article/$', LocationArticleApi.as_view(), name='api-location-article'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += staticfiles_urlpatterns()
