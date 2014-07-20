from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from filebrowser_safe.functions import convert_filename
from django.utils.translation import ugettext_lazy as _
from django.db import models
from zipfile import ZipFile
from StringIO import StringIO
import os
from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable, Orderable
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import FileField
from pari.album.models import ImageCollection, ImageCollectionImage
from pari.article.mixins import AdminThumbMixin

FACES_UPLOAD_DIR = "uploads/faces/"


class District(Displayable):
    district = models.CharField(_("District"), max_length=100, unique=True)
    district_description = models.CharField(_("Description(Optional)"), max_length=255, null=True, blank=True)
    objects = DisplayableManager()

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
        ordering = ("district",)
        app_label = "faces"

    def __unicode__(self):
        return self.district


class Face(Orderable, Displayable, AdminThumbMixin):
    zip_import = models.FileField(verbose_name=_("Zip import"), blank=True,
                                  upload_to=upload_to("faces.Face.zip_import", "faces"),
                                  help_text=_("Upload a zip file containing images, and "
                                              "they'll be imported into this gallery."))
    image_collection = models.ForeignKey(ImageCollection)
    district = models.ForeignKey(District, null=True)
    is_pinned = models.BooleanField(verbose_name="Pin To Top", default=False)
    admin_thumb_field = "image"
    objects = DisplayableManager()

    @models.permalink
    def get_absolute_url(self):
        return "face-detail", (), {"alphabet": self.first_letter_of_district()}

    @property
    def pinned_image(self):
        return self.images.get(is_pinned=True).image_collection_image.file.path

    class Meta:
        verbose_name = _("Face")
        verbose_name_plural = _("Faces")
        ordering = ("district",)

    def first_letter_of_district(self):
        return self.district.district[0].lower()

    def save(self, delete_zip_import=True, *args, **kwargs):
        """
        If a zip file is uploaded, extract any images from it and add
        them to the gallery, before removing the zip file.
        """

        # Update if a entry for district already exists
        face_exist = Face.objects.filter(district=self.district)
        face_exist = face_exist and face_exist[0]
        if not self.pk and face_exist:
            self.image_collection = face_exist.image_collection
            self.image_collection_id = face_exist.image_collection_id
            self.pk = face_exist.pk
            self.site_id = face_exist.site_id

        if not hasattr(self, 'image_collection'):
            new_image_collection = ImageCollection(title=self.district.district)
            new_image_collection.save()
            self.image_collection = new_image_collection
        super(Face, self).save(*args, **kwargs)
        if self.zip_import:
            zip_file = ZipFile(self.zip_import)
            # import PIL in either of the two ways it can end up installed.
            try:
                from PIL import Image
            except ImportError:
                import Image
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    image = Image.open(StringIO(data))
                    image.load()
                    image = Image.open(StringIO(data))
                    image.verify()
                except:
                    continue
                name = convert_filename(os.path.split(name)[1])
                path = os.path.join(FACES_UPLOAD_DIR, self.slug,
                                    name.decode("utf-8"))
                try:
                    saved_path = default_storage.save(path, ContentFile(data))
                except UnicodeEncodeError:
                    from warnings import warn

                    warn("A file was saved that contains unicode "
                         "characters in its path, but somehow the current "
                         "locale does not support utf-8. You may need to set "
                         "'LC_ALL' to a correct value, eg: 'en_US.UTF-8'.")
                    path = os.path.join(FACES_UPLOAD_DIR, self.slug,
                                        unicode(name, errors="ignore"))
                    saved_path = default_storage.save(path, ContentFile(data))
                face_image = FaceImage(image_file=saved_path)
                self.images.add(face_image)
            if delete_zip_import:
                zip_file.close()
                self.zip_import.delete(save=True)


def get_pinned_faces(alphabet):
    return Face.objects.filter(district__district__istartswith=alphabet).filter(is_pinned=True)


def get_pinned_face_images(face):
    return face.images.filter(is_pinned=True)


class FaceImage(Orderable, Displayable):
    face = models.ForeignKey("Face", related_name="images")

    image_collection_image = models.ForeignKey("album.ImageCollectionImage", related_name="face_image")

    is_pinned = models.BooleanField(verbose_name="Pin To Top", default=False)

    image_file = FileField(_("File"), max_length=200, format="Image", null=True,
                           upload_to=upload_to("album.ImageCollection.file", "faces"))

    class Meta:
        verbose_name = _("FaceImage")
        verbose_name_plural = _("FaceImages")
        app_label = "faces"

    def __unicode__(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        name = "face-detail"
        return name, (), {"alphabet": self.face.first_letter_of_district()}

    @property
    def get_thumbnail(self):
        return self.image_collection_image.get_thumbnail

    def save(self, delete_audio_file=True, *args, **kwargs):

        self.gen_description = False

        if not hasattr(self, 'image_collection_image'):
            image_collection_image = ImageCollectionImage(file=self.image_file)
            self.face.image_collection.images.add(image_collection_image)
            self.image_collection_image = image_collection_image
        super(FaceImage, self).save(*args, **kwargs)


def get_face_images_by_district_first_letter(alphabet):
    return FaceImage.objects.filter(face__district__district__istartswith=alphabet).extra(
        select={'upper_district': 'upper(district)'}).order_by('upper_district')
