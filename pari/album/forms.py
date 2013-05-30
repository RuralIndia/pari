from django import forms
from django.core.exceptions import ValidationError


class AlbumImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if not hasattr(self, "cleaned_data"):
            raise ValidationError(u'Invalid cover image')

        if self.instance.zip_import:
            return

        if not self.cleaned_data[0]:
            raise ValidationError(u'Upload atleast one image')

        has_cover = [True for album in self.cleaned_data if album and album['is_cover']]
        if not has_cover:
            raise ValidationError(u'Choose a cover pic')
