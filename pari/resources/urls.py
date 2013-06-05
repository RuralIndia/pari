from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import ResourceDetail, ResourceList


urlpatterns = patterns('pari.resources.views',
                       url(r'^$', ResourceList.as_view(), name='resource-list'),
                       url(r'^(?P<slug>.+)/$', ResourceDetail.as_view(), name='resource-detail'),
                       )

urlpatterns += staticfiles_urlpatterns()
