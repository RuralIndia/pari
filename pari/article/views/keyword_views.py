from django.views.generic.detail import DetailView
from itertools import chain

from mezzanine.generic.models import Keyword

from pari.article.models import Article
from pari.article.mixins import ArticleListMixin
from pari.article.common import get_keyword_articles


class KeywordDetail(ArticleListMixin, DetailView):
    context_object_name = "keyword"
    article_list_context_name = "articles"
    model = Keyword

    def get_article_list_queryset(self):
        return get_keyword_articles(self.object)

    def get_context_data(self, **kwargs):

        context = super(KeywordDetail, self).get_context_data(**kwargs)
        keyword = context['keyword']
        context['topics'] = Article.topics.filter(keywords__keyword__title__in=[keyword])
        assigned_keywords = list(chain.from_iterable(article.keywords.all() for article in context["articles"]))
        context['related_keywords'] = list(set([key.keyword for key in assigned_keywords if key.keyword != keyword][:10]))
        return context
