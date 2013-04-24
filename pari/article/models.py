# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.fields import FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.core.models import Displayable, Ownable, RichText
from mezzanine.generic.fields import CommentsField

from geoposition.fields import GeopositionField

from .managers import ArticleManager, TopicManager


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


class Type(models.Model):
    title = models.CharField(max_length=5)

    def __str__(self):
        return "%s" % (self.title)

    def __unicode__(self):
        return "%s" % (self.title)


class Article(Displayable, Ownable, RichText, AdminThumbMixin):
    location = models.ForeignKey(Location)
    is_topic = models.BooleanField(verbose_name=_("Is a topic?"), default=False)
    category_list = models.ManyToManyField(Category, verbose_name=_("Categories"),
                                           blank=False, null=False, related_name="articles")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("blog.BlogPost.featured_image", "blog"),
        format="Image", max_length=255, null=True, blank=True)

    capsule_video = models.CharField(max_length=100, null=True, blank=True)

    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related Articles"), blank=True)
    types = models.ManyToManyField(Type, related_name="articles", verbose_name="Article Type")

    admin_thumb_field = "featured_image"

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

    @property
    def is_video_article(self):
        return self.types.filter(title__iexact='Video').exists()
