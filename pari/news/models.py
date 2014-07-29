from django.utils.translation import ugettext_lazy as _

from django.db import models
from pari.article.models import Article


class LatestArticle(models.Model):
    new_current_articles = models.ManyToManyField(Article, verbose_name=_("New current articles"), blank=True,
                                                  related_name='new_current_articles')
    new_archive_articles = models.ManyToManyField(Article, verbose_name=_("New archive articles"), blank=True,
                                                  related_name='new_archive_articles')

    class Meta:
        verbose_name = _("Latest article")
        verbose_name_plural = _("Latest articles")
        app_label = 'news'
