from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pari.album.views import AlbumDetail, AlbumList, AlbumImageDetail


urlpatterns = patterns('pari.album.views',
                       url(r'^$', AlbumList.as_view(), name='album-list'),
                       url(r'^(?P<slug>.+)/$', AlbumDetail.as_view(), name='album-detail'),
                       url(r'^(?P<slug>.+)/(?P<order>\d+)$', AlbumImageDetail.as_view(), name='album-image-detail'),
                       )

urlpatterns += staticfiles_urlpatterns()
