from django.utils.translation import ugettext_lazy as _
from django.db import models

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable, Orderable
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import FileField

from pari.article.mixins import AdminThumbMixin


class Face(Orderable, Displayable, AdminThumbMixin):
    image = FileField(verbose_name=_("Image"),
                      upload_to=upload_to("faces.face.image", "face"),
                      format="Image", max_length=255, null=False, blank=False)

    district = models.CharField(_("District"), max_length=255)

    admin_thumb_field = "image"
    objects = DisplayableManager()


    @models.permalink
    def get_absolute_url(self):
        return "face-detail", (), {"slug": self.slug}

    class Meta:
        verbose_name = _("Face")
        verbose_name_plural = _("Faces")

    @property
    def get_thumbnail(self):
        return self.image

    def first_letter(self):
        return self.district[0]

def get_faces_by_first_letter(alphabet):
    return Face.objects.filter(district__startswith=alphabet).extra( select={'upper_district': 'upper(district)'}).order_by('upper_district')