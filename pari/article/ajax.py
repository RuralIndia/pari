from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mezzanine.core.models import Displayable

from mezzanine.generic.models import Keyword

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from .models import Article, Category, Type, Location


@dajaxice_register
def category_article_filter(request, category, filter=None, page=1):
    category = Category.objects.get(pk=category)
    article_queryset = category.articles.all()

    return article_filter(article_queryset, category.title, filter, page)


@dajaxice_register
def location_article_filter(request, location, filter=None, page=1):
    location = Location.objects.get(pk=location)
    article_queryset = location.article_set.all()

    return article_filter(article_queryset, location.title, filter, page)


@dajaxice_register
def keyword_article_filter(request, keyword, filter=None, page=1):
    keyword = Keyword.objects.get(pk=keyword)
    article_queryset = Article.articles.filter(keywords__keyword=keyword)

    return article_filter(article_queryset, keyword.title, filter, page)


def filter_search_result(result_set, query, filter, page):
    if filter is not None:
        result_set = [result for result in result_set if filter == result.__class__.__name__]
    result_types = [subclass.__name__ for subclass in Displayable.__subclasses__() if "pari" in subclass.__module__]
    paginator = Paginator(result_set, 10)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    render = render_to_string('article/includes/search_result_list.html', {'results': results,
                                                                           'query': query,
                                                                           'result_types': result_types})

    dajax = Dajax()
    dajax.assign('#article-list', 'innerHTML', render)
    dajax.script('ArticleFilter.init();')
    return dajax.json()


@dajaxice_register
def search_filter(request, query, filter=None, page=1):
    result_set = Displayable.objects.search(query)

    return filter_search_result(result_set, query, filter, page)


def get_article_list(article_queryset, page, filter):
    if(filter is not None):
        article_queryset = article_queryset.filter(types__title__iexact=filter)

    paginator = Paginator(article_queryset, 10)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return articles


def article_filter(article_queryset, title, filter, page):
    articles = get_article_list(article_queryset, page, filter)
    render = render_to_string('article/includes/article_list.html', {'articles': articles,
                                                                     'title': title,
                                                                     'filter': filter,
                                                                     'types': Type.objects.all()})

    dajax = Dajax()
    dajax.assign('#article-list', 'innerHTML', render)
    dajax.script('ArticleFilter.init();')
    return dajax.json()
