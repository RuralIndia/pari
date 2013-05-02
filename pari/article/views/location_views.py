from django.views.generic.detail import DetailView

from pari.article.models import Location, Article
from pari.article.mixins import ArticleListMixin
from pari.article.common import get_location_articles, get_paginated_list


class LocationDetail(ArticleListMixin, DetailView):
    context_object_name = "location"
    article_list_context_name = "articles_in_location"
    model = Location

    def get_article_list_queryset(self):
        return get_paginated_list(get_location_articles(self.object), page=1)

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)
        location = context['location']
        context['topics_in_location'] = Article.topics.filter(location=location)
        return context
