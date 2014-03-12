from random import randint

from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mezzanine.core.models import Displayable


def get_paginated_list(non_paginated, page):
    paginator = Paginator(non_paginated, 10)

    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated


def get_article_list(article_queryset, page, filter):
    if filter is not None:
        article_queryset = article_queryset.filter(types__title__iexact=filter)

    return get_paginated_list(article_queryset, page)


def is_searchable(subclass):
    return getattr(subclass, 'is_searchable', True)


def get_result_types(filter, display_count=4):
    return [subclass.__name__ for subclass in
            sorted([subclass for subclass in Displayable.__subclasses__()
                    if "pari" in subclass.__module__ and is_searchable(subclass)],
            key=lambda x: type_sort_order(x, filter, display_count), reverse=True)]


def get_random_entries(model, count=1):
    max_id = model.objects.aggregate(Max('id'))['id__max']
    if max_id:
        i = 0
        while i < count:
            try:
                yield model.objects.get(pk=randint(1, max_id))
                i += 1
            except model.DoesNotExist:
                pass
    else:
        pass


def type_sort_order(x, filter, display_count=4):
    defined_order = getattr(x, 'type_filter_order', 0)
    is_filtered = x.__name__ == filter
    if defined_order > 1:
        return defined_order
    if defined_order == 1:
        if is_filtered:
            return defined_order
        else:
            return 0
    if is_filtered:
        return 1
