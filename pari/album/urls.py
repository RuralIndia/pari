from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('pari.album.views',
                       url(r'^$', 'index', name='photos-detail'),
                       url(r'^(?P<slug>.+)/$', 'show', name='album-detail'),
                       )

urlpatterns += staticfiles_urlpatterns()
