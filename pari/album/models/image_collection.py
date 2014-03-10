from string import punctuation
from urllib import unquote

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Orderable
from mezzanine.utils.models import upload_to


class ImageCollection(Displayable):
    zip_import = models.FileField(verbose_name=_("Zip import"), blank=True,
                                  upload_to=upload_to("album.ImageCollection.zip_import", "albums"),
                                  help_text=_("Upload a zip file containing images, and "
                                              "they'll be imported into this collection."))

    type_filter_order = 3

    class Meta:
        verbose_name = _("Image Collection")
        verbose_name_plural = _("Image Collection")
        app_label = "album"

    @models.permalink
    def get_absolute_url(self):
        name = "image-collection-detail"
        return name, (), {"slug": self.slug}


class ImageCollectionImage(Orderable, Displayable):
    image_collection = models.ForeignKey("ImageCollection", related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
                     upload_to=upload_to("album.ImageCollection.file", "albums"))

    class Meta:
        verbose_name = _("ImageCollectionImage")
        verbose_name_plural = _("ImageCollectionImages")
        app_label = "album"

    def __unicode__(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        name = "image-collection-image-detail"
        return name, (), {"slug": self.image_collection.slug, "order": self._order + 1}

    @property
    def get_thumbnail(self):
        return self.file

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        self.gen_description = False

        if not self.id and not self.description:
            name = unquote(self.file.url).split("/")[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(ImageCollectionImage, self).save(*args, **kwargs)
