from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin

from .models import Resource


class ResourceAdmin(DisplayableAdmin):
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "embed_source"],
    }),
    list_display = ("title", "description")
    list_editable = ()
    list_filter = ()


admin.site.register(Resource, ResourceAdmin)
