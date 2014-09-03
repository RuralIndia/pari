from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin

from .models import Resource, Factoid
from pari.resources.forms import ResourceForm
from pari.thirdparty.api.slideshare import get_resource_thumb_url


class FactoidInline(TabularDynamicInlineAdmin):
    model = Factoid
    fk_name = "resource"
    fields = ('image', 'title')


class ResourceAdmin(DisplayableAdmin):
    form = ResourceForm
    fieldsets = (None, {
        "fields": ["title", "date", "authors", "copyright", "focus", "embed_source", "thumbnail_url"],
    }),
    inlines = [
        FactoidInline,
    ]
    list_display = ("title",)
    list_editable = ()
    list_filter = ()

    def save_model(self, request, obj, form, change):
        embed_source = form.cleaned_data.get('embed_source')
        instance = change and Resource.objects.get(pk=obj.id)

        if not change or embed_source != instance.embed_source or not instance.thumbnail_url:
                obj.thumbnail_url = get_resource_thumb_url(embed_source)
        obj.save()


class FactoidAdmin(DisplayableAdmin):
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "image", "external_link"],
    }),
    list_display = ("admin_thumb", "title", "description")
    list_editable = ()
    list_filter = ()


admin.site.register(Resource, ResourceAdmin)
admin.site.register(Factoid, FactoidAdmin)
