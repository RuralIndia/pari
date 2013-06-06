from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from pari.album.models import Album, AlbumImage
from pari.album.forms import AlbumImageInlineFormset


class AlbumImageInline(TabularDynamicInlineAdmin):
    model = AlbumImage
    extra = 15
    formset = AlbumImageInlineFormset


class AlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumImageInline, ]
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "keywords", "zip_import", "articles", "predominant_tone"],
    }),

    list_display = ("title",)

    class Media:
        css = {"all": ("mezzanine/css/admin/gallery.css",)}
        js = ("/static/album/js/admin.js",)

admin.site.register(Album, AlbumAdmin)
