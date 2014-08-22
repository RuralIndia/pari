from django import forms
from pari.article.forms import TinyMceWidget
from pari.resources.models import Resource


class ResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['authors'].widget = TinyMceWidget(attrs={'rows': 2, 'cols': 5})
        self.fields['copyright'].widget = TinyMceWidget(attrs={'rows': 2, 'cols': 5})
        self.fields['focus'].widget = TinyMceWidget(attrs={'rows': 10, 'cols': 20})
        self.fields['thumbnail_url'].widget = forms.TextInput(attrs={'style': 'width:70%', 'readonly': 'readonly'})

    class Meta:
        model = Resource
