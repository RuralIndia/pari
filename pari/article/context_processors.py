from .models import Type
from django.contrib.sites.models import RequestSite


def types(request):
    return {'types': Type.objects.all()}

def sites(request):
    return {'site': RequestSite(request)}
