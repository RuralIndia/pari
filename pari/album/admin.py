from django.contrib import admin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from pari.album.models import Album, AlbumImage
from pari.album.forms import AlbumImageInlineFormset, AlbumForm


class AlbumImageInline(TabularDynamicInlineAdmin):
    model = AlbumImage
    extra = 15
    formset = AlbumImageInlineFormset
    fieldsets = (None, {
        "fields": ["file", "description", "audio", "photographer", "location", "publish_date", "is_cover", "_order"],
    }),


class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    inlines = [AlbumImageInline, ]
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "meta_data",
                   "publish_date", "keywords", "zip_import", "location",
                   "photographer", "articles", "predominant_tone"],
    }),

    list_display = ("title",)

    class Media:
        css = {"all": ("mezzanine/css/admin/gallery.css",)}
        js = ("/static/album/js/admin.js",)

admin.site.register(Album, AlbumAdmin)
