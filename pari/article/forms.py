from django import forms

from .models import Location, Category


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
