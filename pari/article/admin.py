from copy import deepcopy
from django.contrib import admin

from mezzanine.blog.models import BlogPost
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.core.admin import DisplayableAdmin

from .models import Article, Location, Category
from .forms import LocationForm, CategoryForm

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"].insert(1, "category_list")
blog_fieldsets[0][1]["fields"].remove("categories")
blog_fieldsets[0][1]["fields"].insert(-1, "location")
blog_fieldsets[0][1]["fields"].insert(-1, "is_topic")

blog_list_display = deepcopy(BlogPostAdmin.list_display)
blog_list_display.insert(-1, "is_topic")


class ArticleAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets
    list_display = blog_list_display
    list_filter = ()
    filter_horizontal = ("category_list", "related_posts",)


class LocationAdmin(DisplayableAdmin):
    form = LocationForm
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "location"],
    }),
    list_display = ("title", "description", "location")
    list_editable = ()
    list_filter = ()


class CategoryAdmin(DisplayableAdmin):
    form = CategoryForm
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "image"],
    }),
    list_display = ("admin_thumb", "title", "description")
    list_editable = ()
    list_filter = ()


admin.site.unregister(BlogPost)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
