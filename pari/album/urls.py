from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pari.album.views import AlbumDetail, AlbumList, AlbumImageDetail, ImageCollectionImageList


urlpatterns = patterns('pari.album.views',
                       url(r'^$', AlbumList.as_view(), name='album-list'),
                       url(r'^(?P<slug>.+)/$', AlbumDetail.as_view(), name='album-detail'),
                       url(r'^(?P<slug>.+)/(?P<order>\d+)$', AlbumImageDetail.as_view(), name='album-image-detail'),
                       url(r'^(?P<slug>.+)/all$', ImageCollectionImageList.as_view(), name='image-collection-image-list'),
                       )

urlpatterns += staticfiles_urlpatterns()
