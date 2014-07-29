from django.contrib import admin
from mezzanine.core.admin import SingletonAdmin
from pari.news.models import LatestArticle
from pari.news.forms import LatestArticleForm


class LatestArticleAdmin(SingletonAdmin):
    form = LatestArticleForm
    filter_horizontal = ('new_current_articles', 'new_archive_articles')

admin.site.register(LatestArticle, LatestArticleAdmin)
