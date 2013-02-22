from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LocationList, LocationDetail, LocationArticle

urlpatterns = patterns('pari.article.views',
    url(r'^api/$', 'api_root'),
    url(r'^api/locations/$', LocationList.as_view(), name='location-list'),
    url(r'^api/locations/(?P<pk>[0-9.,]+)/$', LocationDetail.as_view(), name='location-detail'),
    url(r'^api/locations/(?P<pk>[0-9.,]+)/article/$', LocationArticle.as_view(), name='location-article'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
