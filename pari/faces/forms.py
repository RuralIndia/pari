from django import forms
from django.core.exceptions import ValidationError
from pari.article.forms import TinyMceWidget
from pari.faces.models import District, Face


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District


class FaceForm(forms.ModelForm):
    class Meta:
        model = Face


class FaceImageInlineFormset(forms.models.BaseInlineFormSet):

    def add_fields(self, form, index):
        super(FaceImageInlineFormset, self).add_fields(form, index)
        form.fields['description'] = forms.CharField(max_length=1000, required=True, widget=TinyMceWidget(attrs={'rows': 15, 'cols': 20}))

    def clean(self):
        if self.instance.zip_import:
            del self.errors[:]
            return

        if any(self.errors):
            return

        if not any(self.cleaned_data):
            raise ValidationError(u'Upload at the least one image to the album.')
