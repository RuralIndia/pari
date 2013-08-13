from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable
from pari.article.mixins import AdminThumbMixin


class Contribution(Displayable, AdminThumbMixin):
    icon = models.CharField(max_length=20, blank=True)

    objects = DisplayableManager()

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")
        app_label = "contribution"
        ordering = ['pk']

    @models.permalink
    def get_absolute_url(self):
        name = "contribution-detail"
        return (name, (), {"slug": self.slug})

    @property
    def get_thumbnail(self):
        return ""
