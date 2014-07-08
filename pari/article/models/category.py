from django.utils.translation import ugettext_lazy as _
from django.db import models

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable, Orderable
from mezzanine.utils.models import upload_to
from mezzanine.core.fields import FileField

from pari.article.mixins import AdminThumbMixin


class Category(Orderable, Displayable, AdminThumbMixin):
    image = FileField(verbose_name=_("Image"),
                      upload_to=upload_to("article.Category.image", "category"),
                      format="Image", max_length=255, null=False, blank=True)

    admin_thumb_field = "image"

    objects = DisplayableManager()
    search_fields = {"title": 10, "description": 5}

    type_filter_order = 1

    @models.permalink
    def get_absolute_url(self):
        return ("category-detail", (), {"slug": self.slug})

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("_order", "title",)
        app_label = "article"

    @property
    def get_thumbnail(self):
        return self.image
