from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from pari.article.models import Article, get_archive_articles, get_all_articles
from pari.article.mixins import ArticleListMixin
from pari.article.templatetags.article_filters import month_name


class ArticleDetail(DetailView):
    context_object_name = "blog_post"
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = context['blog_post']
        context['related_articles'] = article.related_posts.all()[:5]
        return context


class ArchiveDetail(ArticleListMixin, ListView):
    context_object_name = "articles"
    model = Article
    template_name = 'article/archive_detail.html'

    def get_article_list_queryset(self):
        self.year = self.kwargs['year']
        self.month = self.kwargs['month']
        return get_archive_articles(self.month, self.year)

    def get_context_data(self, **kwargs):
        context = super(ArchiveDetail, self).get_context_data(**kwargs)
        context['year'] = self.year
        context['month'] = self.month
        context['month_as_name'] = month_name(self.month)
        context['title'] = "{0} {1}".format(context['month_as_name'], self.year)
        return context


class ArticleList(ArticleListMixin, ListView):
    context_object_name = "articles"
    model = Article

    def get_article_list_queryset(self):
        return get_all_articles()

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['title'] = "All articles"
        return context
