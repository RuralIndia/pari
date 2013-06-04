from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pari.contribution.views import ContributionDetail, ContributionList


urlpatterns = patterns('pari.contribution.views',
                       url(r'^$', ContributionList.as_view(), name='contribution-list'),
                       url(r'^(?P<slug>.+)/$', ContributionDetail.as_view(), name='contribution-detail'),
                       )

urlpatterns += staticfiles_urlpatterns()
