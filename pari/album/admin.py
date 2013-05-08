from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from pari.album.models import Album, AlbumImage


class AlbumImageInline(TabularDynamicInlineAdmin):
    model = AlbumImage
    extra = 5

class AlbumAdmin(admin.ModelAdmin):
    inlines = [ AlbumImageInline, ]
    fieldsets = (None, {
        "fields": ["title", "description","keywords"],
        }),

    class Media:
        css = {"all": ("mezzanine/css/admin/gallery.css",)}

admin.site.register(Album, AlbumAdmin)
