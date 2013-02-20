# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogPost
from geoposition.fields import GeopositionField


class Article(BlogPost):
    location = GeopositionField("Location")

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-publish_date",)
