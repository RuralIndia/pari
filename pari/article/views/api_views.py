from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from pari.article.serializers import LocationSerializer, LocationArticleSerializer
from pari.article.models import Location, get_locations_with_published_articles


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'locations': reverse('api-location-list', request=request),
    })


class LocationListApi(generics.ListAPIView):
    queryset = get_locations_with_published_articles()
    serializer_class = LocationSerializer


class LocationDetailApi(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationSerializer


class LocationArticleApi(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationArticleSerializer
