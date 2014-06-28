from django.forms.models import inlineformset_factory
from django.test import TestCase
from factory import DjangoModelFactory, SubFactory, Sequence
from pari.faces.admin import FaceAdmin, FaceImageInline
from pari.faces.forms import FaceImageInlineFormset, FaceForm
from pari.faces.models import FaceImage, Face, District, get_pinned_faces, get_pinned_face_images, \
    get_face_images_by_district_first_letter
from pari.album.tests import ImageCollectionImageFactory


class DistrictFactory(DjangoModelFactory):
    FACTORY_FOR = District
    district = Sequence(lambda n: 'A-{0}'.format(n))


class FaceFactory(DjangoModelFactory):
    FACTORY_FOR = Face
    district = SubFactory(DistrictFactory)


class FaceImageFactory(DjangoModelFactory):
    FACTORY_FOR = FaceImage

    title = 'face image'
    face = SubFactory(FaceFactory)
    description = 'description 1'
    image_collection_image = SubFactory(ImageCollectionImageFactory)


class FaceAdminTest(TestCase):
    def setUp(self):
        self.faceImage = FaceImageFactory()
        self.face = self.faceImage.face

    def setup_formset(self, data, face):
        FaceImageFactoryFormset = inlineformset_factory(Face, FaceImage, formset=FaceImageInlineFormset,
                                                        fields=('image_file', 'is_pinned', 'title', 'description',
                                                                '_order'))
        return FaceImageFactoryFormset(data, prefix='form', instance=face)

    def test_admin_includes_zip_import(self):
        self.assertIn("zip_import", FaceAdmin.fieldsets[0][1]['fields'])

    def test_admin_includes_district(self):
        self.assertIn("district", FaceAdmin.fieldsets[0][1]['fields'])

    def test_admin_includes_faceimage_inline(self):
        self.assertIn(FaceImageInline, FaceAdmin.inlines)

    def test_face_is_invalid_if_image_is_not_uploaded(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-_order': u'1',
            'form-0-title': u'Image 1',
            'form-0-description': u'Description',
        }
        formset = self.setup_formset(data, self.face)
        self.assertFalse(formset.is_valid())
        keys = [key for errors in formset.errors for key in errors.keys()]
        self.assertTrue(any(keys))
        self.assertIn('image_file', keys)

    def test_face_is_invalid_if_description_is_not_specified(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-_order': u'1',
            'form-0-title': u'Image 1',
            'form-0-image_file': u'image.jpg'
        }
        formset = self.setup_formset(data, self.face)
        self.assertFalse(formset.is_valid())
        keys = [key for error in formset.errors for key in error.keys()]
        self.assertTrue(any(keys))
        self.assertIn('description', keys)

    def test_face_is_invalid_if_district_is_not_specified(self):
        self.face.district = DistrictFactory(district='')
        face_form = FaceForm(instance=self.face)
        self.assertFalse(face_form.is_valid())

    def test_face_is_valid_if_atleast_one_image_is_uploaded(self):
        data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-_order': u'1',
            'form-0-image_file': u'image.jpg',
            'form-0-title': u'Image 1',
            'form-0-description': u'description',
        }
        formset = self.setup_formset(data, self.face)
        self.assertTrue(formset.is_valid())


class FaceTest(TestCase):
    def setUp(self):
        self.face_image = FaceImageFactory()
        self.face = self.face_image.face

    def test_first_letter_of_face(self):
        face = FaceFactory(district=DistrictFactory(district="district"))
        self.assertEquals("d", face.first_letter_of_district())

    def create_face(self, is_pinned=False):
        face = FaceFactory()
        face.is_pinned = is_pinned
        face.save()
        return face

    def create_face_image(self, is_pinned=False):
        face_image = FaceImageFactory()
        face_image.is_pinned = is_pinned
        face_image.save()
        return face_image

    def test_get_pinned_faces(self):
        face1 = self.create_face(is_pinned=True)
        self.create_face(is_pinned=True)
        self.create_face(is_pinned=False)

        self.assertEqual(2, len(get_pinned_faces(face1.first_letter_of_district())))

    def test_get_pinned_face_images(self):
        face_image1 = self.create_face_image(is_pinned=True)
        face_image2 = self.create_face_image(is_pinned=True)
        face_image3 = self.create_face_image(is_pinned=False)

        face = face_image1.face
        face.images.add(face_image2)
        face.images.add(face_image3)
        self.assertEqual(2, len(get_pinned_face_images(face_image2.face)))

    def test_get_face_images_by_district_first_letter(self):
        face_image1 = self.create_face_image()
        face_image2 = self.create_face_image()

        face = face_image1.face
        face.district = DistrictFactory(district='Test District')
        face.images.add(face_image2)
        face.save()

        self.assertEqual(2, len(get_face_images_by_district_first_letter(face.first_letter_of_district())))
