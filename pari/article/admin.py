from copy import deepcopy
from django.contrib import admin
from mezzanine.blog.models import BlogPost
from mezzanine.blog.admin import BlogPostAdmin
from .models import Article, Location

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"].insert(-1, "location")
blog_fieldsets[0][1]["fields"].insert(-1, "is_topic")

blog_list_display = deepcopy(BlogPostAdmin.list_display)
blog_list_display.insert(-1, "is_topic")


class ArticleAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets
    list_display = blog_list_display


admin.site.unregister(BlogPost)
admin.site.register(Location)
admin.site.register(Article, ArticleAdmin)
