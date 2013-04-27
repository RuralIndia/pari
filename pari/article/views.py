from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from mezzanine.core.models import Displayable

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from mezzanine.utils.views import render
from mezzanine.generic.models import Keyword

from .models import Location, Article, Category
from .serializers import LocationSerializer, LocationArticleSerializer
from .ajax import get_article_list


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'locations': reverse('api-location-list', request=request),
    })


class LocationListApi(generics.ListAPIView):
    model = Location
    serializer_class = LocationSerializer


class LocationDetailApi(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationSerializer


class LocationArticleApi(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationArticleSerializer


class LocationDetail(DetailView):
    context_object_name = "location"
    model = Location

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)
        location = context['location']
        all_articles = Article.articles.filter(location=location)
        page = self.request.GET.get('page')
        filter = self.request.GET.get('filter')
        context['articles_in_location'] = get_article_list(all_articles, page, filter)
        context['topics_in_location'] = Article.topics.filter(location=location)
        return context


class CategoriesList(ListView):
    context_object_name = "categories"
    model = Category


class CategoryDetail(DetailView):
    context_object_name = "category"
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        all_articles = context['category'].articles.filter(is_topic=False)
        page = self.request.GET.get('page')
        filter = self.request.GET.get('filter')
        context['articles'] = get_article_list(all_articles, page, filter)
        return context


class ArticleDetail(DetailView):
    context_object_name = "blog_post"
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = context['blog_post']
        context['related_articles'] = article.related_posts.all()[:5]
        return context


class KeywordDetail(DetailView):
    context_object_name = "keyword"
    model = Keyword

    def get_context_data(self, **kwargs):

        context = super(KeywordDetail, self).get_context_data(**kwargs)
        keyword = context['keyword']
        context['articles_by_keyword'] = Article.articles.filter(keywords__keyword__title__in=[keyword])
        context['topics_by_keyword'] = Article.topics.filter(keywords__keyword__title__in=[keyword])
        assigned_keywords = list(chain.from_iterable(article.keywords.all() for article in context["articles_by_keyword"]))
        context['related_keywords'] = list(set([key.keyword for key in assigned_keywords if key.keyword != keyword][:10]))
        return context


def search_detail(request):
    query = request.GET.get("q", "")
    articles = Displayable.objects.search(query)
    templates = [u"article/search_detail.html"]
    c = {"query": query, "articles": articles}
    return render(request, templates, c)


def topic_detail(request, slug):
    blog_posts = Article.topics.published(for_user=request.user).select_related()
    return blog_detail(blog_posts, request, slug)


def article_detail(request, slug):
    blog_posts = Article.articles.published(for_user=request.user).select_related()
    return blog_detail(blog_posts, request, slug)


def blog_detail(blog_posts, request, slug, template="blog/blog_post_detail.html"):
    blog_post = get_object_or_404(blog_posts, slug=slug)
    context = {"blog_post": blog_post, "editable_obj": blog_post}
    templates = [u"blog/blog_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)
