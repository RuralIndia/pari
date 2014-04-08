from factory import DjangoModelFactory, SubFactory
from pari.album.models import ImageCollection, ImageCollectionImage


class ImageCollectionFactory(DjangoModelFactory):
    FACTORY_FOR = ImageCollection

    title = 'Image Collection'


class ImageCollectionImageFactory(DjangoModelFactory):
    FACTORY_FOR = ImageCollectionImage

    title = 'Image 1'
    description = 'Image Collection Image'
    image_collection = SubFactory(ImageCollectionFactory)
