from django.utils.translation import ugettext_lazy as _

from django.db import models
from mezzanine.blog.models import BlogPost
from geoposition.fields import GeopositionField

# Create your models here.

class Article(BlogPost):
    location = GeopositionField("Location")

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-publish_date",)
