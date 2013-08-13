from mezzanine.conf import settings

if "haystack" in settings.INSTALLED_APPS:
    from haystack import indexes

    from pari.album.models import Album, AlbumImage
    from pari.article.models import Location, Author, Category
    from pari.contribution.models import Contribution
    from pari.resources.models import Resource, Factoid


    class DisplayableIndex(indexes.SearchIndex, indexes.Indexable):
        text = indexes.CharField(document=True, use_template=True)
        title = indexes.CharField(model_attr='title')
        description = indexes.CharField(model_attr='description')
        get_absolute_url = indexes.CharField()
        get_thumbnail = indexes.CharField()

        model = None
        haystack_use_for_indexing = False

        def prepare_get_absolute_url(self, obj):
            return obj.get_absolute_url()

        def prepare_get_thumbnail(self, obj):
            return unicode(obj.get_thumbnail)

        def get_model(self):
            return self.model

        def index_queryset(self, using=None):
            return self.get_model().objects.filter()


    class LocationIndex(DisplayableIndex):
        location = indexes.CharField(model_attr='location')

        model = Location
        haystack_use_for_indexing = True


    class AlbumIndex(DisplayableIndex):
        photographer = indexes.CharField(model_attr='photographer')
        image = indexes.CharField(model_attr='cover')

        model = Album
        haystack_use_for_indexing = True


    class AlbumImageIndex(DisplayableIndex):
        photographer = indexes.CharField(model_attr='photographer')
        album = indexes.CharField()

        def prepare_album(self, obj):
            return obj.album.title

        model = AlbumImage
        haystack_use_for_indexing = True


    class AuthorIndex(DisplayableIndex):
        model = Author
        haystack_use_for_indexing = True


    class CategoryIndex(DisplayableIndex):
        model = Category
        haystack_use_for_indexing = True


    class ContributionIndex(DisplayableIndex):
        model = Contribution
        haystack_use_for_indexing = True


    class ResourceIndex(DisplayableIndex):
        model = Resource
        haystack_use_for_indexing = True


    class FactoidIndex(DisplayableIndex):
        model = Factoid
        haystack_use_for_indexing = True
