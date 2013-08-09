from random import randint

from django.db.models import get_models, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mezzanine.core.models import Displayable
from mezzanine.conf import settings

from haystack.query import SearchQuerySet


def get_paginated_list(non_paginated, page):
    paginator = Paginator(non_paginated, 10)

    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated


class HaystackSearch(object):
    queryset = SearchQuerySet()

    @staticmethod
    def get_search_results(query, filter=None):
        queried_set = HaystackSearch.queryset.filter(content=query)
        if filter is not None:
            search_model = next(model for model in get_models() if issubclass(model, Displayable) and model.__name__==filter)
            return queried_set.models(search_model)
        return queried_set

    @staticmethod
    def get_atom_name(result):
        return result.model_name


class MezzanineSearch(object):
    @staticmethod
    def get_search_results(query, filter=None):
        if filter is not None:
            search_model = next(model for model in get_models() if issubclass(model, Displayable) and model.__name__==filter)
            results = search_model.objects.search(query)
        else:
            results = Displayable.objects.search(query)
        return results

    @staticmethod
    def get_atom_name(result):
        return result.__class__.__name__.lower()


searcher = MezzanineSearch
if 'haystack' in settings.INSTALLED_APPS:
    searcher = HaystackSearch


def get_search_results(query, filter=None, page=1):
    search_results = searcher.get_search_results(query, filter)
    return get_paginated_list(search_results, page)


def get_article_list(article_queryset, page, filter):
    if filter is not None:
        article_queryset = article_queryset.filter(types__title__iexact=filter)

    return get_paginated_list(article_queryset, page)


def get_result_types(filter, display_count=4):
    return [subclass.__name__ for subclass in
            sorted([subclass for subclass in Displayable.__subclasses__()
                    if "pari" in subclass.__module__],
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
