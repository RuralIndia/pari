from django import forms
from pari.news.models import LatestArticle


class LatestArticleForm(forms.ModelForm):
    class Meta:
        model = LatestArticle
