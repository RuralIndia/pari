from django import forms
from django.core.exceptions import ValidationError

from pari.album.models import Album
from pari.article.forms import DisplayableForm, TinyMceWidget


class AlbumImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if self.instance.zip_import:
            del self.errors[:]
            return

        if any(self.errors):
            return

        if not any(self.cleaned_data):
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


class AlbumForm(DisplayableForm):
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['meta_data'].widget = TinyMceWidget(attrs={'rows': 10, 'cols': 20})

    def clean(self):
        cleaned_data = super(AlbumForm, self).clean()
        if cleaned_data['zip_import'] and not (cleaned_data['location'] and cleaned_data['photographer']):
            raise ValidationError(u'Specify photographer and location when doing zip import')

        return cleaned_data

    class Meta:
        model = Album
