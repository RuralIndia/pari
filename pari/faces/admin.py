from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin
from pari.faces.forms import DistrictForm, FaceForm, FaceImageInlineFormset
from pari.faces.models import District, Face, FaceImage


class DistrictAdmin(DisplayableAdmin):
    form = DistrictForm
    fieldsets = (None, {
        "fields": ["district", "district_description"],
    }),
    list_display = ("district", "district_description")
    list_display_links = ("district", )
    list_editable = ()


class FaceImageInline(TabularDynamicInlineAdmin):
    model = FaceImage
    formset = FaceImageInlineFormset
    extra = 1

    fieldsets = (None, {
        "fields": ["image_file", "title", "is_pinned", "description", "_order"],
    }),


class FaceAdmin(DisplayableAdmin):
    form = FaceForm
    inlines = [FaceImageInline, ]
    fieldsets = (None, {
        "fields": ["district", "is_pinned", "zip_import", ],
    }),
    list_display = ("admin_thumb", "district", "is_pinned")
    list_display_links = ("district", )
    list_editable = ()
    list_filter = ()

admin.site.register(Face, FaceAdmin)
admin.site.register(District, DistrictAdmin)
