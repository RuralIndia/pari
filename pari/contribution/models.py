from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.fields import FileField
from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable
from pari.article.mixins import AdminThumbMixin


class Contribution(Displayable, AdminThumbMixin):
    image = FileField(verbose_name=_("Image"),
                     format="Image", max_length=255, null=True, blank=True)
    admin_thumb_field = "image"

    objects = DisplayableManager()

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")
        app_label = "contribution"

    @models.permalink
    def get_absolute_url(self):
        name = "contribution-detail"
        return (name, (), {"slug": self.slug})
