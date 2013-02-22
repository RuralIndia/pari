from .models import Location
from rest_framework import serializers
from rest_framework.fields import Field


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    latLng = Field(source='get_as_latLng')

    class Meta:
        model = Location
        fields = ('name', 'latLng')
