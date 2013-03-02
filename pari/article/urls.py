from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LocationList, LocationDetail, LocationArticle

urlpatterns = patterns('pari.article.views',
    url(r'^api/$', 'api_root'),
    url(r'^api/locations/$', LocationList.as_view(), name='api-location-list'),
    url(r'^api/locations/(?P<pk>\d+)/$', LocationDetail.as_view(), name='api-location-detail'),
    url(r'^api/locations/(?P<pk>\d+)/article/$', LocationArticle.as_view(), name='api-location-article'),
    url(r'^topics/(?P<slug>.+)/$', 'topic_detail', name='topic-detail'),
    url(r'^locations/(?P<slug>.+)/$', 'location_detail', name='location-detail'),
    url(r'^categories/(?P<slug>.+)/$', 'category_detail', name='category-detail'),
    url(r'^(?P<slug>.+)/$', 'article_detail', name='article-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
