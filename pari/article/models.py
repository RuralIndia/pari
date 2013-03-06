# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import ArticleManager, TopicManager

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.blog.models import BlogPost
from geoposition.fields import GeopositionField


class Location(Displayable):
    location = GeopositionField("Location")

    objects = DisplayableManager()
    search_fields = {"title": 10, "description": 5}

    def get_as_latLng(self):
        return unicode(self.location).split(',')

    def get_articles(self):
        return self.article_set.filter(is_topic=False)[:5]

    def get_topics(self):
        return self.article_set.filter(is_topic=True)[:5]

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.location)

    @models.permalink
    def get_absolute_url(self):
        return ("location-detail", (), {"slug": unicode(self.slug)})


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


class Article(BlogPost):
    location = models.ForeignKey(Location)
    is_topic = models.BooleanField(verbose_name=_("Is a topic?"), default=False)
    category_list = models.ManyToManyField(Category, verbose_name=_("Categories"),
                    blank=False, null=False, related_name="articles")

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
