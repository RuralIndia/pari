from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import SearchList

urlpatterns = patterns('pari.search.views',
    url(r'^$', SearchList.as_view(), name='search-detail'),

)

urlpatterns += staticfiles_urlpatterns()
