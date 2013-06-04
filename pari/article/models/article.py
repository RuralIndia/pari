from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.template.defaultfilters import truncatewords

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText
from mezzanine.generic.fields import CommentsField

from pari.article.managers import ArticleManager, TopicManager
from pari.article.mixins import AdminThumbMixin

from .category import Category
from .location import Location
from .type import Type


class Article(Displayable, Ownable, RichText, AdminThumbMixin):
    locations = models.ManyToManyField(Location, verbose_name=_("Locations"))
    is_topic = models.BooleanField(verbose_name=_("Is a topic?"), default=False)
    category_list = models.ManyToManyField(Category, verbose_name=_("Categories"),
                                           blank=False, null=False, related_name="articles")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        format="Image", max_length=255, null=True, blank=True)

    author = models.ForeignKey("Author", related_name='articles')

    capsule_video = models.CharField(max_length=100, null=True, blank=True)

    featured_video = models.CharField(max_length=100, null=True, blank=True)

    featured_audio = models.CharField(max_length=100, null=True, blank=True)

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
        app_label = "article"

    @models.permalink
    def get_absolute_url(self):
        name = "article-detail"
        if self.is_topic:
            name = "topic-detail"
        return (name, (), {"slug": self.slug})

    @property
    def is_video_article(self):
        return self.types.filter(title__iexact='Video').exists()

    @property
    def get_thumbnail(self):
        return self.featured_image

    @property
    def short_description(self):
        return truncatewords(self.description, 20)


def get_category_articles(category):
    return category.articles.filter(is_topic=False)


def get_location_articles(location):
    return Article.articles.filter(locations__location=location.location)


def get_keyword_articles(keyword):
    return Article.articles.filter(keywords__keyword=keyword)


def get_author_articles(author):
    return Article.articles.filter(author=author)


def get_archive_articles(month, year):
    return Article.objects.filter(publish_date__year=year, publish_date__month=month)
