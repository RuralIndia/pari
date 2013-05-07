from django.utils.translation import ugettext_lazy as _
from django.db import models

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.core.fields import FileField


class Category(Displayable, AdminThumbMixin):
    image = FileField(verbose_name=_("Image"),
                      upload_to=upload_to("article.Category.image", "category"),
                      format="Image", max_length=255, null=False, blank=False)

    admin_thumb_field = "image"

    objects = DisplayableManager()
    search_fields = {"title": 10, "description": 5}

    @models.permalink
    def get_absolute_url(self):
        return ("category-detail", (), {"slug": self.slug})

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("title",)
        app_label = "article"

    @property
    def get_thumbnail(self):
        return self.image
