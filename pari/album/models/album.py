from StringIO import StringIO
import inspect
import os
from zipfile import ZipFile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser_safe.functions import convert_filename
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Orderable
from mezzanine.utils.models import upload_to
from pari.album.helpers.sound_cloud_helper import SoundCloudHelper

from pari.album.models import ImageCollection, ImageCollectionImage
from pari.article.models import Article, Location


ALBUMS_UPLOAD_DIR = "uploads/albums/"


class Album(Displayable):
    zip_import = models.FileField(verbose_name=_("Zip import"), blank=True,
                                  upload_to=upload_to("album.Album.zip_import", "albums"),
                                  help_text=_("Upload a zip file containing images, and "
                                              "they'll be imported into this gallery."))

    articles = models.ManyToManyField(Article, blank=True)
    location = models.ForeignKey(Location, related_name='albums', blank=True, null=True)
    photographer = models.ForeignKey("article.Author", related_name='albums', blank=True, null=True)

    meta_data = models.CharField(verbose_name=_("About the album"), max_length=200, blank=True)

    image_collection = models.ForeignKey(ImageCollection)

    TONE_CHOICES = (
        ('grey', 'Greyscale'),
        ('colour', 'Colour')
    )

    TONE_DEFAULT = 'colour'

    predominant_tone = models.CharField(max_length=10,
                                        choices=TONE_CHOICES,
                                        default=TONE_DEFAULT)

    type_filter_order = 3

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")
        app_label = "album"

    @models.permalink
    def get_absolute_url(self):
        name = "album-detail"
        return name, (), {"slug": self.slug}

    @property
    def cover(self):
        if self.images.all().count() > 0:
            return self.images.get(is_cover=True).image_collection_image.file.path

    @property
    def get_thumbnail(self):
        return self.cover

    @property
    def has_cover(self):
        return self.images.filter(is_cover=True).exists()

    @property
    def get_cover(self):
        return self.images.get(is_cover=True)

    def save(self, delete_zip_import=True, *args, **kwargs):
        """
        If a zip file is uploaded, extract any images from it and add
        them to the gallery, before removing the zip file.
        """

        if not hasattr(self, 'image_collection'):
            new_image_collection = ImageCollection(title=self.title)
            new_image_collection.save()
            self.image_collection = new_image_collection
            # audio = [album_image.audio_file for album_image in self.images.all() if album_image.audio_file]
            # if(any(audio)):
            #     soundcloud_helper = SoundCloudHelper()
            #     soundcloud_helper.create_playlist(self.title)
        super(Album, self).save(*args, **kwargs)
        if self.zip_import:
            zip_file = ZipFile(self.zip_import)
            # import PIL in either of the two ways it can end up installed.
            try:
                from PIL import Image
            except ImportError:
                import Image
            first = True
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
                path = os.path.join(ALBUMS_UPLOAD_DIR, self.slug,
                                    name.decode("utf-8"))
                try:
                    saved_path = default_storage.save(path, ContentFile(data))
                except UnicodeEncodeError:
                    from warnings import warn

                    warn("A file was saved that contains unicode "
                         "characters in its path, but somehow the current "
                         "locale does not support utf-8. You may need to set "
                         "'LC_ALL' to a correct value, eg: 'en_US.UTF-8'.")
                    path = os.path.join(ALBUMS_UPLOAD_DIR, self.slug,
                                        unicode(name, errors="ignore"))
                    saved_path = default_storage.save(path, ContentFile(data))
                album_image = AlbumImage(image_file=saved_path, location=self.location,
                                         photographer=self.photographer)
                if first and not self.has_cover:
                    album_image.is_cover = True
                    first = False
                self.images.add(album_image)
            if delete_zip_import:
                zip_file.close()
                self.zip_import.delete(save=True)


class AlbumImage(Orderable, Displayable):
    album = models.ForeignKey("Album", related_name="images")
    image_collection_image = models.ForeignKey("ImageCollectionImage", related_name="album_image")
    audio = models.CharField(max_length=30, null=True, blank=True)
    audio_file = models.FileField(_("File"), max_length=200, null=True, blank=True,
                                  upload_to=upload_to("album.AlbumImage.audio_file", "albums"))
    is_cover = models.BooleanField(verbose_name="Album cover", default=False)
    photographer = models.ForeignKey("article.Author", related_name='photographs')
    location = models.ForeignKey(Location, verbose_name=_("Location"))
    image_file = FileField(_("File"), max_length=200, format="Image", null=True,
                           upload_to=upload_to("album.ImageCollection.file", "albums"))

    class Meta:
        verbose_name = _("AlbumImage")
        verbose_name_plural = _("AlbumImages")
        app_label = "album"

    def __unicode__(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        name = "album-image-detail"
        return name, (), {"slug": self.album.slug, "order": self._order + 1}

    @property
    def get_thumbnail(self):
        return self.image_collection_image.get_thumbnail

    def save(self, delete_audio_file=True, *args, **kwargs):

        image_collection_image = ImageCollectionImage.objects.filter(file=self.image_file, image_collection_id=self.album.image_collection.id).first()
        if not image_collection_image:
            self.add_to_image_collection()
        else:
            self.image_collection_image = image_collection_image

        super(AlbumImage, self).save(*args, **kwargs)
        if self.audio_file:
            soundcloud_helper = SoundCloudHelper()
            audio_file_id = soundcloud_helper.upload(self.audio_file, self.album.title)
            self.audio = audio_file_id
            if delete_audio_file:
                self.audio_file.delete(save=True)

    def add_to_image_collection(self):
        image_collection_image = ImageCollectionImage(file=self.image_file)
        self.album.image_collection.images.add(image_collection_image)
        self.image_collection_image = image_collection_image
