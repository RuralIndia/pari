from StringIO import StringIO
import os
from string import punctuation
from urllib import unquote
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Orderable
from mezzanine.utils.models import upload_to
from mezzanine.galleries.models import GALLERIES_UPLOAD_DIR

from zipfile import ZipFile

from pari.article.models import Article


class Album(Displayable):
    zip_import = models.FileField(verbose_name=_("Zip import"), blank=True,
        upload_to=upload_to("galleries.Gallery.zip_import", "galleries"),
        help_text=_("Upload a zip file containing images, and "
                    "they'll be imported into this gallery."))

    articles = models.ManyToManyField(Article, blank=True)

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    @models.permalink
    def get_absolute_url(self):
        name = "album-detail"
        return (name, (), {"slug": self.slug})

    @property
    def cover(self):
        return self.images.get(is_cover=True).file.path

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
                name = os.path.split(name)[1]
                path = os.path.join(GALLERIES_UPLOAD_DIR, self.slug,
                                    name.decode("utf-8"))
                try:
                    saved_path = default_storage.save(path, ContentFile(data))
                except UnicodeEncodeError:
                    from warnings import warn
                    warn("A file was saved that contains unicode "
                         "characters in its path, but somehow the current "
                         "locale does not support utf-8. You may need to set "
                         "'LC_ALL' to a correct value, eg: 'en_US.UTF-8'.")
                    path = os.path.join(GALLERIES_UPLOAD_DIR, self.slug,
                                        unicode(name, errors="ignore"))
                    saved_path = default_storage.save(path, ContentFile(data))
                album_image = AlbumImage(file=saved_path)
                if first and not self.has_cover:
                    album_image.is_cover = True
                    first = False
                self.images.add(album_image)
            if delete_zip_import:
                zip_file.close()
                self.zip_import.delete(save=True)


class AlbumImage(Orderable):
    album = models.ForeignKey("Album", related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
                     upload_to=upload_to("galleries.GalleryImage.file", "galleries"))
    description = models.CharField(_("Description"), max_length=1000,
                                   blank=True)
    audio = models.CharField(max_length=100, null=True, blank=True)
    is_cover = models.BooleanField(verbose_name="Album cover", default=False)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description:
            name = unquote(self.file.url).split("/")[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(AlbumImage, self).save(*args, **kwargs)
