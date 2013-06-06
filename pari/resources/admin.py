from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin

from .models import Resource, Factoid


class FactoidInline(TabularDynamicInlineAdmin):
    model = Factoid
    fk_name = "resource"
    fields = ('image', 'title')


class ResourceAdmin(DisplayableAdmin):
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "embed_source"],
    }),
    inlines = [
        FactoidInline,
    ]
    list_display = ("title", "description")
    list_editable = ()
    list_filter = ()


class FactoidAdmin(DisplayableAdmin):
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "image"],
    }),
    list_display = ("admin_thumb", "title", "description")
    list_editable = ()
    list_filter = ()


admin.site.register(Resource, ResourceAdmin)
admin.site.register(Factoid, FactoidAdmin)
