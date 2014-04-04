from copy import deepcopy
from django.contrib import admin

from mezzanine.blog.models import BlogPost
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin

from .models import Article, ArticleCarouselImage, Location, Category, Type, Author
from .forms import LocationForm, CategoryForm, TypeForm, AuthorForm

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"].insert(1, "category_list")
blog_fieldsets[0][1]["fields"].insert(1, "types")
blog_fieldsets[0][1]["fields"].insert(1, "author")
blog_fieldsets[0][1]["fields"].insert(7, "capsule_video")
blog_fieldsets[0][1]["fields"].insert(7, "featured_video")
blog_fieldsets[0][1]["fields"].insert(7, "featured_audio")
blog_fieldsets[0][1]["fields"].remove("categories")
blog_fieldsets[0][1]["fields"].insert(-1, "locations")
blog_fieldsets[0][1]["fields"].insert(-1, "is_topic")

blog_list_display = deepcopy(BlogPostAdmin.list_display)
blog_list_display.insert(-1, "is_topic")


class ArticleCarouselImageInline(TabularDynamicInlineAdmin):
    model = ArticleCarouselImage
    extra = 15
    fieldsets = (None, {
        "fields": ["file", "title", "description"],
    }),


class ArticleAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets
    inlines = [ArticleCarouselImageInline, ]
    list_display = blog_list_display
    list_filter = ()
    filter_horizontal = ("category_list", "related_posts", "locations")


class TypeAdmin(admin.ModelAdmin):
    form = TypeForm
    fieldsets = (None, {
        "fields": ["title", "icon_class"],
    }),


class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "image", "location"],
    }),
    list_display = ("title", "description", "image", "location")
    list_editable = ()
    list_filter = ()


class CategoryAdmin(DisplayableAdmin):
    form = CategoryForm
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "image", "_order"],
    }),
    list_display = ("admin_thumb", "title", "description", "_order")
    list_editable = ()
    list_filter = ()


class AuthorAdmin(DisplayableAdmin):
    form = AuthorForm
    fieldsets = (None, {
        "fields": ["title", "image", "description"],
    }),

admin.site.register(Type, TypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
