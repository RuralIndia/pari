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


def get_article_list(article_queryset, page, filter):
    if filter is not None:
        article_queryset = article_queryset.filter(types__title__iexact=filter)

    return get_paginated_list(article_queryset, page)


def article_filter(article_queryset, title, filter, page):
    articles = get_article_list(article_queryset, page, filter)

    return render_dajax_response('article/includes/article_list.html', {'articles': articles,
                                                                        'title': title,
                                                                        'filter': filter,
                                                                        'types': Type.objects.all()})


def get_paginated_list(non_paginated, page):
    paginator = Paginator(non_paginated, 10)

    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated


def render_dajax_response(template, context):
    render = render_to_string(template, context)

    dajax = Dajax()
    dajax.assign('.filter-list-container', 'innerHTML', render)
    dajax.script('ArticleFilter.init();')
    return dajax.json()
