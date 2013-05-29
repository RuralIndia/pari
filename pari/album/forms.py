from django import forms
from django.core.exceptions import ValidationError


class AlbumImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if not self.cleaned_data[0] and not self.instance.zip_import:
            raise ValidationError(u'Upload atleast one image')
