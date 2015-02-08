from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import translation
from django.conf import settings

from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

from pari.article.models import Article, get_archive_articles, get_all_articles, ArticleCarouselImage
from pari.article.mixins import ArticleListMixin
from pari.article.templatetags.article_filters import month_name

# TODO: Remove in django 1.7+
LANGUAGE_SESSION_KEY = "django_language"


class ArticleDetail(DetailView):
    context_object_name = "blog_post"
    model = Article

    def get_queryset(self):
        if self.request.user.is_staff:
            return Article.objects.prefetch_related('locations', 'carousel_images')
        else:
            return Article.articles.prefetch_related('locations', 'carousel_images')

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = context['blog_post']
        translations = []
        for language in settings.LANGUAGES[1:]:
            content = getattr(article, "content_{0}".format(language[0]), None)
            if content and content.strip():
                translations.append(language)
        language = self.request.GET.get("hl")
        if language and language in [ii[0] for ii in settings.LANGUAGES]:
            translation.activate(language)
            self.request.session[LANGUAGE_SESSION_KEY] = language
        context['translations'] = translations
        context['related_articles'] = article.related_posts.filter(status=CONTENT_STATUS_PUBLISHED)[:5]
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


class ArticleCarouselImageDetail(DetailView):
    context_object_name = "image"
    model = ArticleCarouselImage

    def get_object(self, queryset=None):
        return ArticleCarouselImage.objects.get(article__slug=self.kwargs['slug'], _order=int(self.kwargs['order']) - 1)
