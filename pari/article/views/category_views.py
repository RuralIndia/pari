from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from pari.article.models import Category
from pari.article.mixins import ArticleListMixin
from pari.article.common import get_category_articles


class CategoriesList(ListView):
    context_object_name = "categories"
    model = Category


class CategoryDetail(ArticleListMixin, DetailView):
    context_object_name = "category"
    model = Category

    def get_article_list_queryset(self):
        return get_category_articles(self.object)
