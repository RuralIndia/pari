from django.contrib import admin
from django import forms
from mezzanine.core.admin import TabularDynamicInlineAdmin
from pari.album.models import Album, AlbumImage
from pari.album.forms import AlbumImageInlineFormset


class AlbumImageInline(TabularDynamicInlineAdmin):
    model = AlbumImage
    extra = 15
    formset = AlbumImageInlineFormset
    widget = {
        'is_cover': forms.RadioSelect
    }

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(AlbumImageInline, self).get_formset(request, obj, **kwargs)
        return formset


class AlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumImageInline, ]
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "audio", "keywords", "zip_import"],
    }),

    list_display = ("title", "description")

    class Media:
        css = {"all": ("mezzanine/css/admin/gallery.css",)}
        js = ("/pari/static/album/js/admin.js",)

admin.site.register(Album, AlbumAdmin)
