# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mezzanine.blog.models import BlogPost
from geoposition.fields import GeopositionField


class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    location = GeopositionField("Location", primary_key=True)

    def get_as_latLng(self):
        return unicode(self.location).split(',')

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.location)


class Article(BlogPost):
    location = models.ForeignKey(Location)

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-publish_date",)
