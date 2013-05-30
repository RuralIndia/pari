from django import forms

from .models import Location, Category, Type, Author


class DisplayableForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    description = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    gen_description = forms.BooleanField(initial=False, required=False)


class LocationForm(DisplayableForm):
    class Meta:
        model = Location


class CategoryForm(DisplayableForm):
    class Meta:
        model = Category


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type


class AuthorForm(DisplayableForm):
    class Meta:
        model = Author


class TinyMceWidget(forms.Textarea):

    class Media:
        js = ('js/tinymce/tinymce.min.js', 'js/tinymce_setup.js')
        css = {
            'all': ('css/tinymce_overrides.css',),
        }

    def __init__(self, *args, **kwargs):
        super(TinyMceWidget, self).__init__(*args, **kwargs)
        self.attrs["class"] = "mceEditor"
