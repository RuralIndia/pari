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
