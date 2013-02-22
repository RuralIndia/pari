from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LocationList, LocationDetail

urlpatterns = patterns('pari.article.views',
    url(r'^$', 'api_root'),
    url(r'^locations$', LocationList.as_view(), name='location-list'),
    url(r'^locations/(?P<pk>\d+)/$', LocationDetail.as_view(), name='location-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
