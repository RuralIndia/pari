from django import forms
from django.core.exceptions import ValidationError


class AlbumImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if self.instance.zip_import:
            return

        if any(self.errors):
            return

        if not self.cleaned_data:
            raise ValidationError(u'Upload at the least one image to the album.')

        if not self.has_cover():
            raise ValidationError(u'Choose a cover image')

    def save(self):
        if self.has_cover() and self.instance.has_cover:
            cover = self.instance.get_cover
            if not self.submitted_cover()[0]['id'] == cover:
                cover.is_cover = False
            cover.save()
        super(AlbumImageInlineFormset, self).save()

    def has_cover(self):
        return any(self.submitted_cover())

    def submitted_cover(self):
        return [image for image in self.cleaned_data if image and image['is_cover']]
