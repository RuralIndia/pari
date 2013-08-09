from haystack import indexes
from .models import Location


class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    location = indexes.CharField(model_attr='location')
    get_absolute_url = indexes.CharField()

    def prepare_get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_model(self):
        return Location

    def index_queryset(self, using=None):
        return self.get_model().objects.filter()
