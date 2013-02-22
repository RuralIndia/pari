from .models import Location
from .serializers import LocationSerializer, LocationArticleSerializer

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'locations': reverse('location-list', request=request),
    })


class LocationList(generics.ListAPIView):
    model = Location
    serializer_class = LocationSerializer


class LocationDetail(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationSerializer


class LocationArticle(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationArticleSerializer
