from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pari.album.views import AlbumDetail, AlbumList


urlpatterns = patterns('pari.album.views',
                       url(r'^$', AlbumList.as_view(), name='album-list'),
                       url(r'^(?P<slug>.+)/$', AlbumDetail.as_view(), name='album-detail'),
                       )

urlpatterns += staticfiles_urlpatterns()
