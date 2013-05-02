from django.template.loader import render_to_string

from mezzanine.core.models import Displayable
from mezzanine.generic.models import Keyword

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from .models import Category, Type, Location
from .common import get_category_articles, get_location_articles, get_keyword_articles
from .common import get_paginated_list, get_article_list


@dajaxice_register
def category_article_filter(request, category, filter=None, page=1):
    category = Category.objects.get(pk=category)
    article_queryset = get_category_articles(category)

    return article_filter(article_queryset, category.title, filter, page)


@dajaxice_register
def location_article_filter(request, location, filter=None, page=1):
    location = Location.objects.get(pk=location)
    article_queryset = get_location_articles(location)

    return article_filter(article_queryset, location.title, filter, page)


@dajaxice_register
def keyword_article_filter(request, keyword, filter=None, page=1):
    keyword = Keyword.objects.get(pk=keyword)
    article_queryset = get_keyword_articles(keyword)

    return article_filter(article_queryset, keyword.title, filter, page)


@dajaxice_register
def search_filter(request, query, filter=None, page=1):
    result_set = Displayable.objects.search(query)

    return filter_search_result(result_set, query, filter, page)


def filter_search_result(result_set, query, filter, page):
    if filter is not None:
        result_set = [result for result in result_set if filter == result.__class__.__name__]
    result_types = [subclass.__name__ for subclass in Displayable.__subclasses__() if "pari" in subclass.__module__]

    results = get_paginated_list(result_set, page)

    return render_dajax_response('article/includes/search_result_list.html', {'results': results,
                                                                              'query': query,
                                                                              'filter': filter,
                                                                              'result_types': result_types})


def article_filter(article_queryset, title, filter, page):
    articles = get_article_list(article_queryset, page, filter)

    return render_dajax_response('article/includes/article_list.html', {'articles': articles,
                                                                        'title': title,
                                                                        'filter': filter,
                                                                        'types': Type.objects.all()})


def render_dajax_response(template, context):
    render = render_to_string(template, context)

    dajax = Dajax()
    dajax.assign('.filter-list-container', 'innerHTML', render)
    dajax.script('ArticleFilter.init();')
    return dajax.json()
