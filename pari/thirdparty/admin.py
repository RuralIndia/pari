from copy import deepcopy

from django.contrib import admin

from mezzanine.pages.models import Link
from mezzanine.pages.admin import LinkAdmin

fieldsets = deepcopy(LinkAdmin.fieldsets)
fieldsets[0][1]["fields"].insert(2, "html_class")


class CustomLinkAdmin(LinkAdmin):
    fieldsets = fieldsets

admin.site.unregister(Link)
admin.site.register(Link, CustomLinkAdmin)