from django import forms
from pari.news.models import NewsPost, NewsCategory, LatestArticle


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost


class NewsCategoryForm(forms.ModelForm):
    class Meta:
        model = NewsCategory


class LatestArticleForm(forms.ModelForm):
    class Meta:
        model = LatestArticle
