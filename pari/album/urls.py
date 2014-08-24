from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from pari.album.models import get_all_albums, get_other_albums, get_talking_albums
from pari.album.views import AlbumDetail, AlbumList, AlbumImageDetail, ImageCollectionImageList


urlpatterns = patterns('pari.album.views',
                       url(r'^$', AlbumList.as_view(), {'albums': get_all_albums}, name='album-list'),
                       url(r'^talking/$', AlbumList.as_view(), {'albums': get_talking_albums}, name='talking-album-list'),
                       url(r'^other/$', AlbumList.as_view(), {'albums': get_other_albums}, name='other-album-list'),

                       url(r'^talking/(?P<slug>.+)/$', AlbumDetail.as_view(), name='talking-album-detail'),
                       url(r'^other/(?P<slug>.+)/$', AlbumDetail.as_view(), name='other-album-detail'),
                       url(r'^(?P<slug>.+)/$', AlbumDetail.as_view(), name='album-detail'),

                       url(r'^(?P<slug>.+)/(?P<order>\d+)$', AlbumImageDetail.as_view(), name='album-image-detail'),
                       url(r'^(?P<slug>.+)/all$', ImageCollectionImageList.as_view(), name='image-collection-image-list'),
                       )

urlpatterns += staticfiles_urlpatterns()
