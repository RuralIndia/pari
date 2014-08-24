
from django.forms.models import inlineformset_factory
from django.test import TestCase

import factory
import mock

from pari.album.models import get_all_albums, get_talking_albums, get_other_albums
from pari.album.admin import AlbumAdmin, AlbumImageInline
from pari.album.forms import AlbumImageInlineFormset
from pari.album.models import Album, AlbumImage, ImageCollection, ImageCollectionImage
from pari.article.tests import LocationFactory, AuthorFactory


class AlbumFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Album

    title = 'Album 1'
    photographer = factory.SubFactory(AuthorFactory)


class ImageCollectionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ImageCollection

    title = 'Image Collection'


class ImageCollectionImageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ImageCollectionImage

    title = 'Image 1'
    description = 'Image Collection Image'
    image_collection = factory.SubFactory(ImageCollectionFactory)


class AlbumImageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AlbumImage

    title = 'Image 1'
    image_file = 'gallery.png'
    audio = 'audio id'
    _order = 1
    album = factory.SubFactory(AlbumFactory)
    image_collection_image = factory.SubFactory(ImageCollectionImageFactory)
    location = factory.SubFactory(LocationFactory)
    photographer = factory.SubFactory(AuthorFactory)


class AlbumBuild:
    def __init__(self):
        self.album = AlbumFactory.create()

    def add_album_image(self, **kwargs):
        AlbumImageFactory(album=self.album, **kwargs)
        return self


class AlbumTests(TestCase):
    def setUp(self):
        AlbumBuild().add_album_image().add_album_image()
        AlbumBuild().add_album_image().add_album_image(audio='')
        AlbumBuild().add_album_image().add_album_image(audio=None)
        AlbumBuild().add_album_image(audio='').add_album_image(audio='')
        AlbumBuild().add_album_image(audio=None).add_album_image(audio=None)
        AlbumBuild().add_album_image(audio=None).add_album_image(audio='')
        AlbumBuild().add_album_image(audio=None).add_album_image(audio='   ')

    def test_get_all_albums(self):
        self.assertEqual(7, get_all_albums().count())

    def test_get_talking_albums(self):
        self.assertEqual(3, get_talking_albums().count())

    def test_get_other_albums(self):
        self.assertEqual(4, get_other_albums().count())


class AlbumAdminTests(TestCase):
    def setUp(self):
        self.albumImage = AlbumImageFactory()
        self.album = self.albumImage.album

    def setup_formset(self, data, album):
        AlbumImageFactoryFormset = inlineformset_factory(Album, AlbumImage, formset=AlbumImageInlineFormset,
                                                         fields=(
                                                             'image_file', 'is_cover', 'location', 'photographer',
                                                             'title', 'status', '_order'))
        return AlbumImageFactoryFormset(data, prefix='form', instance=album)

    def test_admin_includes_zip_import(self):
        self.assertIn("zip_import", AlbumAdmin.fieldsets[0][1]['fields'])

    def test_admin_includes_image_inline(self):
        self.assertIn(AlbumImageInline, AlbumAdmin.inlines)

    def test_album_is_invalid_if_it_has_no_image(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
        }
        formset = self.setup_formset(data, AlbumFactory())
        self.assertFalse(formset.is_valid())

    def test_album_is_valid_if_an_image_is_uploaded_as_cover(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-image_file': u'file.png',
            'form-0-is_cover': u'True',
            'form-0-location': self.albumImage.location.id,
            'form-0-photographer': self.albumImage.photographer.id,
            'form-0-title': u'1',
            'form-0-status': u'1',
            'form-0-_order': u'1',
        }
        formset = self.setup_formset(data, self.album)
        self.assertTrue(formset.is_valid())
        self.assertEqual(len(formset.non_form_errors()), 0)

    def test_album_is_invalid_if_no_image_is_chosen_as_cover(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-image_file': u'file.png',
            'form-0-location': self.albumImage.location.id,
            'form-0-photographer': self.albumImage.photographer.id,
            'form-0-title': u'1',
            'form-0-status': u'2',
            'form-0-_order': u'1',
        }
        formset = self.setup_formset(data, self.album)
        self.assertFalse(formset.is_valid())
        self.assertIn('Choose a cover image', formset.non_form_errors())

    def test_album_is_invalid_if_image_is_not_uploaded_but_cover_is_checked(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-_order': u'1',
            'form-0-photographer': u'1',
            'form-0-location': u'1',
            'form-0-title': u'1',
            'form-0-status': u'1',
            'form-0-is_cover': u'True',
        }
        formset = self.setup_formset(data, self.album)
        self.assertFalse(formset.is_valid())
        keys = [key for error in formset.errors for key in error.keys()]
        self.assertTrue(any(keys))
        self.assertIn("image_file", keys)

    def test_image1_is_chosen_as_cover_image_if_a_zip_file_and_image1_are_attached_at_the_same_time(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-image_file': u'file.png',
            'form-0-is_cover': u'True',
            'form-0-location': self.albumImage.location.id,
            'form-0-photographer': self.albumImage.photographer.id,
            'form-0-title': u'1',
            'form-0-status': u'1',
            'form-0-_order': u'1',
        }
        self.album.zip_import = mock.Mock(return_value="file.zip")
        formset = self.setup_formset(data, self.album)
        self.assertTrue(formset.is_valid())
        formset.save()
        self.assertEqual(formset.instance.cover, 'file.png')
