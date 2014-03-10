from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from pari.faces.forms import FaceForm
from pari.faces.models import Face

class FaceAdmin(DisplayableAdmin):
    form = FaceForm
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "image", "district"],
    }),
    list_display = ("admin_thumb", "title", "description", "district")
    list_editable = ()
    list_filter = ()

admin.site.register(Face, FaceAdmin)
