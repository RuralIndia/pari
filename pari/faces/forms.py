from django import forms
from pari.article.forms import DisplayableForm, TinyMceWidget
from pari.faces.models import Face


class FaceForm(DisplayableForm):
    description = forms.CharField(max_length=2000, required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))

    def __init__(self, *args, **kwargs):
        super(FaceForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = TinyMceWidget(attrs={'rows': 10, 'cols': 20})

    class Meta:
        model = Face
