from copy import deepcopy
from django.contrib import admin
from mezzanine.blog.models import BlogPost
from mezzanine.blog.admin import BlogPostAdmin
from .models import Article

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"].insert(-1, "location")

class ArticleAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets

admin.site.register(Article, ArticleAdmin)
