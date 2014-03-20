from django import forms
from django.core.exceptions import ValidationError
from pari.article.forms import DisplayableForm, TinyMceWidget
from pari.faces.models import Face


class FaceForm(DisplayableForm):
    description = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))

    def __init__(self, *args, **kwargs):
        super(FaceForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = TinyMceWidget(attrs={'rows': 10, 'cols': 20})

    class Meta:
        model = Face


class FaceImageInlineFormset(forms.models.BaseInlineFormSet):
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
        super(FaceImageInlineFormset, self).save()

    def has_cover(self):
        return any(self.submitted_cover())

    def submitted_cover(self):
        return [image for image in self.cleaned_data if image and image['is_cover']]
