from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable
from mezzanine.core.fields import FileField

from pari.article.mixins import AdminThumbMixin


class Resource(Displayable):
    embed_source = models.CharField(max_length=100)

    objects = DisplayableManager()
    search_fields = {"title": 10, "description": 5}

    type_filter_order = 2

    @models.permalink
    def get_absolute_url(self):
        return ("resource-detail", (), {"slug": self.slug})

    @property
    def get_thumbnail(self):
        return ""

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
        ordering = ("title",)
        app_label = "resources"


class Factoid(Displayable, AdminThumbMixin):
    resource = models.ForeignKey("Resource", related_name="factoids", null=True, blank=True)
    image = FileField(verbose_name=_("Image"),
                      format="Image", max_length=255, null=True, blank=True)

    admin_thumb_field = "image"
    external_link = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        if self.resource:
            return reverse("resource-detail", kwargs={"slug": self.resource.slug})
        else:
            return self.external_link

    @property
    def get_thumbnail(self):
        return ""

    class Meta:
        verbose_name = _("Factoid")
        verbose_name_plural = _("Factoids")
        ordering = ("title",)
        app_label = "resources"
