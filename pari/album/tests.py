from django.forms.models import inlineformset_factory
from django.test import TestCase
import factory
import mock
from pari.album.admin import AlbumAdmin, AlbumImageInline
from pari.album.forms import AlbumImageInlineFormset
from pari.album.models import Album, AlbumImage


class AlbumFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Album

    title = 'Album 1'


class AlbumImageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AlbumImage

    title = 'Image 1'
    file = 'gallery.png'
    _order = 1
    album = factory.SubFactory(AlbumFactory)


class AlbumAdminTests(TestCase):
    def setUp(self):
        self.album = AlbumFactory()

    def test_includes_zip_import(self):
        self.assertIn("zip_import", AlbumAdmin.fieldsets[0][1]['fields'])

    def test_includes_image_inline(self):
        self.assertIn(AlbumImageInline, AlbumAdmin.inlines)

    def setup_formset(self, data, album):
        AlbumImageFactoryFormset = inlineformset_factory(Album, AlbumImage, formset=AlbumImageInlineFormset)
        formset = AlbumImageFactoryFormset(data, prefix='form', instance=album)
        return formset

    def test_album_is_invalid_if_it_has_no_image(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
        }
        formset = self.setup_formset(data, self.album)
        self.assertFalse(formset.is_valid())
        self.assertEqual(len(formset.non_form_errors()), 1)
        self.assertIn("Choose a cover image", formset.non_form_errors())

    def test_album_is_valid_if_zip_file_is_attached(self):
        album_with_zip_file = AlbumFactory()
        album_with_zip_file.zip_import = mock.Mock(return_value="file.zip")
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
        }
        formset = self.setup_formset(data, album_with_zip_file)
        self.assertTrue(formset.is_valid())
        self.assertEqual(len(formset.non_form_errors()), 0)

    def test_album_is_valid_if_an_image_is_uploaded_as_cover(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-file': u'file.png',
            'form-0-is_cover': u'True',
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
            'form-0-file': u'file.png',
            'form-0-_order': u'1',
        }
        formset = self.setup_formset(data, self.album)
        self.assertFalse(formset.is_valid())
        self.assertEqual(len(formset.non_form_errors()), 1)
        self.assertIn("Choose a cover image", formset.non_form_errors())

    def test_album_is_invalid_if_image_is_not_uploaded_but_cover_is_checked(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-_order': u'1',
            'form-0-is_cover': u'True',
        }
        formset = self.setup_formset(data, self.album)
        self.assertFalse(formset.is_valid())
        keys = [key for error in formset.errors for key in error.keys()]
        self.assertEqual(len(keys), 1)
        self.assertIn("file", keys)

    def test_image1_is_chosen_as_cover_image_if_a_zip_file_and_image1_are_attached_at_the_same_time(self):
        album_with_zip_file = AlbumFactory()
        album_with_zip_file.zip_import = mock.Mock(return_value="file.zip")
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-file': u'file.png',
            'form-0-is_cover': u'True',
            'form-0-_order': u'1',
        }
        formset = self.setup_formset(data, album_with_zip_file)
        formset.save()
        self.assertEqual(formset.instance.cover, 'file.png')
