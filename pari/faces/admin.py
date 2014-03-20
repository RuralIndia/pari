from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin
from pari.faces.forms import FaceForm, FaceImageInlineFormset
from pari.faces.models import Face, FaceImage


class FaceImageInline(TabularDynamicInlineAdmin):
    model = FaceImage
    extra = 15
    formset = FaceImageInlineFormset
    fieldsets = (None, {
        "fields": ["image_file", "description", "is_cover", "_order"],
    }),


class FaceAdmin(DisplayableAdmin):
    form = FaceForm
    inlines = [FaceImageInline, ]
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "district", "zip_import", ],
    }),
    list_display = ("admin_thumb", "title", "district")
    list_editable = ()
    list_filter = ()

admin.site.register(Face, FaceAdmin)
