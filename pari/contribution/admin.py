from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from pari.contribution.forms import ContributionForm
from pari.contribution.models import Contribution


class ContributionAdmin(DisplayableAdmin):
    form = ContributionForm
    fieldsets = (None, {
        "fields": ["title", "description", "gen_description", "image"],
    }),
    list_display = ("admin_thumb", "title",)
    list_editable = ()
    list_filter = ()

admin.site.register(Contribution, ContributionAdmin)
