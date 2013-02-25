# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import ArticleManager, TopicManager

from mezzanine.core.managers import DisplayableManager
from mezzanine.blog.models import BlogPost
from geoposition.fields import GeopositionField


class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    location = GeopositionField("Location", primary_key=True)

    def get_as_latLng(self):
        return unicode(self.location).split(',')

    def get_articles(self):
        return self.article_set.filter(is_topic=False)[:5]

    def get_topics(self):
        return self.article_set.filter(is_topic=True)[:5]

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.location)

    @models.permalink
    def get_absolute_url(self):
        return ("location-detail", (), {"pk": unicode(self.location)})


class Article(BlogPost):
    location = models.ForeignKey(Location)
    is_topic = models.BooleanField(verbose_name=_("Is a topic?"), default=False)

    objects = DisplayableManager()
    articles = ArticleManager()
    topics = TopicManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-publish_date",)

    @models.permalink
    def get_absolute_url(self):
        name = "article-detail"
        if self.is_topic:
            name = "topic-detail"
        return (name, (), {"slug": self.slug})
