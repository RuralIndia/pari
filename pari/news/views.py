from django.views.generic import ListView
from pari.news.models import LatestArticle


class LatestArticleList(ListView):
    model = LatestArticle
