from django.db.models import get_models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mezzanine.core.models import Displayable

from .models import Article


def get_category_articles(category):
    return category.articles.filter(is_topic=False)


def get_location_articles(location):
    return Article.articles.filter(location=location)


def get_keyword_articles(keyword):
    return Article.articles.filter(keywords__keyword=keyword)


def get_paginated_list(non_paginated, page):
    paginator = Paginator(non_paginated, 10)

    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated


def get_search_results(query, filter=None, page=1):
    if filter is not None:
        search_model = next(model for model in get_models() if issubclass(model, Displayable) and model.__name__==filter)
        results = search_model.objects.search(query)
    else:
        results = Displayable.objects.search(query)
    return get_paginated_list(results, page)


def get_article_list(article_queryset, page, filter):
    if filter is not None:
        article_queryset = article_queryset.filter(types__title__iexact=filter)

    return get_paginated_list(article_queryset, page)
