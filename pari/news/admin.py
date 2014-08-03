from copy import deepcopy

from django.contrib import admin

from mezzanine.core.admin import SingletonAdmin
from mezzanine.blog.admin import DisplayableAdmin, BlogPostAdmin

from pari.news.models import NewsPost, NewsCategory, LatestArticle
from pari.news.forms import NewsPostForm, NewsCategoryForm, LatestArticleForm

news_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
news_fieldsets[0][1]["fields"].extend(["categories", "content", "allow_comments"])

news_list_display = list(deepcopy(BlogPostAdmin.list_display))
if "admin_thumb" in news_list_display:
    news_list_display.remove("admin_thumb")


class NewsPostAdmin(BlogPostAdmin):
    form = NewsPostForm
    fieldsets = news_fieldsets
    list_display = news_list_display
    filter_horizontal = ("categories",)
    list_filter = ()


class NewsCategoryAdmin(admin.ModelAdmin):
    model = NewsCategoryForm
    fieldsets = ((None, {"fields": ("title",)}),)


class LatestArticleAdmin(SingletonAdmin):
    form = LatestArticleForm
    filter_horizontal = ('new_current_articles', 'new_archive_articles')

admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(LatestArticle, LatestArticleAdmin)
