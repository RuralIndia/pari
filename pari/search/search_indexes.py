from mezzanine.conf import settings
from mezzanine.core.models import Displayable
from pari.faces.models import FaceImage
from pari.news.models import NewsPost

if "haystack" in settings.INSTALLED_APPS:
    from haystack import indexes

    from pari.album.models import Album, AlbumImage
    from pari.article.models import Article, Location, Author, Category

    class DisplayableIndex(indexes.SearchIndex, indexes.Indexable):
        text = indexes.CharField(document=True, use_template=True)
        title = indexes.CharField()
        description = indexes.CharField()
        get_absolute_url = indexes.CharField()
        get_thumbnail = indexes.CharField()

        model = Displayable
        haystack_use_for_indexing = True

        def prepare_get_absolute_url(self, obj):
            return obj.get_absolute_url()

        def prepare_get_thumbnail(self, obj):
            return unicode(getattr(obj, 'get_thumbnail', None) or '')

        def get_model(self):
            return self.model

        def index_queryset(self, using=None):
            return self.get_model().objects.published()

        def should_update(self, instance, **kwargs):
            if instance.get_status_display() == "Published":
                return True
            return False

    class ArticleIndex(DisplayableIndex):
        get_location_titles = indexes.CharField()
        author = indexes.CharField(model_attr='author')
        short_description = indexes.CharField()
        title = indexes.CharField(model_attr='title')
        thumbnail_image_text = indexes.CharField(model_attr='thumbnail_image_text')
        model = Article
        haystack_use_for_indexing = True

        def prepare_get_location_titles(self, obj):
            return obj.get_location_titles

        def prepare_short_description(self, obj):
            return obj.short_description

    class LocationIndex(DisplayableIndex):
        location = indexes.CharField(model_attr='location')
        title = indexes.CharField(model_attr='title')
        description = indexes.CharField(model_attr='description')
        model = Location
        haystack_use_for_indexing = True

    class AlbumIndex(DisplayableIndex):
        photographer = indexes.CharField(model_attr='photographer')
        description = indexes.CharField(model_attr='description')
        title = indexes.CharField(model_attr='title')
        model = Album
        haystack_use_for_indexing = True

    class FaceImageIndex(DisplayableIndex):
        description = indexes.CharField(model_attr='description')
        district = indexes.CharField()
        title = indexes.CharField(model_attr='title')
        model = FaceImage
        haystack_use_for_indexing = True

        def prepare_district(self, obj):
            return obj.face.district.district

    class AlbumImageIndex(DisplayableIndex):
        photographer = indexes.CharField(model_attr='photographer')
        album = indexes.CharField()
        description = indexes.CharField(model_attr='description')

        def prepare_album(self, obj):
            return obj.album.title

        model = AlbumImage
        haystack_use_for_indexing = True

    class AuthorIndex(DisplayableIndex):
        title = indexes.CharField(model_attr='title')
        description = indexes.CharField(model_attr='description')
        model = Author
        haystack_use_for_indexing = True

    class CategoryIndex(DisplayableIndex):
        title = indexes.CharField(model_attr='title')
        description = indexes.CharField(model_attr='description')
        model = Category
        haystack_use_for_indexing = True

    class NewsPostIndex(DisplayableIndex):
        title = indexes.CharField(model_attr='title')
        description = indexes.CharField(model_attr='description')
        thumbnail_image_text = indexes.CharField(model_attr='thumbnail_image_text')
        model = NewsPost
        haystack_use_for_indexing = True
