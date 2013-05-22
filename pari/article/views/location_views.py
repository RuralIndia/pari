from django.views.generic.detail import DetailView

from pari.article.models import Location, Article, get_location_articles
from pari.article.mixins import ArticleListMixin


class LocationDetail(ArticleListMixin, DetailView):
    context_object_name = "location"
    article_list_context_name = "articles"
    model = Location

    def get_article_list_queryset(self):
        return get_location_articles(self.object)

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)
        location = context['location']
        context['topics_in_location'] = Article.topics.filter(locations__location__contains=location.location)
        return context
