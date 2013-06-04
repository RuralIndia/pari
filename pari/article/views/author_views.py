from django.views.generic.detail import DetailView

from pari.article.models import Author, get_author_articles
from pari.article.mixins import ArticleListMixin


class AuthorDetail(ArticleListMixin, DetailView):
    context_object_name = "author"
    model = Author

    def get_article_list_queryset(self):
        return get_author_articles(self.object)
