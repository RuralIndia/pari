from django.db.models import get_models

from mezzanine.core.models import Displayable
from mezzanine.conf import settings

from haystack.query import SearchQuerySet

from pari.article.common import get_paginated_list


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
