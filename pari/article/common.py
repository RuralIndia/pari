from django.db.models import get_models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mezzanine.core.models import Displayable
from mezzanine.conf import settings

import boto
from boto.s3.key import Key

from .models import Article


def get_category_articles(category):
    return category.articles.filter(is_topic=False)


def get_location_articles(location):
    return Article.articles.filter(locations__location=location)


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


def upload_to_s3(key, file_path=None, in_memory_file=None):
    conn = boto.connect_s3()
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    k = Key(bucket)
    k.key = "/media/" + key
    if file_path:
        k.set_contents_from_filename(file_path)
    elif in_memory_file:
        k.set_contents_from_string(in_memory_file.read())
    k.make_public()
