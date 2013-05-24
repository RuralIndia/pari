from string import punctuation
from urllib import unquote

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Orderable
from mezzanine.utils.models import upload_to


class Album(Displayable):

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    @models.permalink
    def get_absolute_url(self):
        name = "album-detail"
        return (name, (), {"slug": self.slug})

    @property
    def get_thumbnail(self):
        return self.images.all()[0].file.path


class AlbumImage(Orderable):

    album = models.ForeignKey("Album", related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
                     upload_to=upload_to("galleries.GalleryImage.file", "galleries"))
    description = models.CharField(_("Description"), max_length=1000,
                                   blank=True)
    audio = models.CharField(max_length=100, null=True, blank=True)

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
