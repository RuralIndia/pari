from django.conf.urls import patterns, url

urlpatterns = patterns('pari.map.views',
    url(r'^$', 'index'),
)
