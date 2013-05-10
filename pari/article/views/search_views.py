from django.views.generic.list import ListView

from mezzanine.core.models import Displayable

from pari.article.common import get_search_results


class SearchList(ListView):
    context_object_name = "results"
    template_name = 'article/search_list.html'

    def get_queryset(self):
        query = self.request.GET.get("query")
        filter = self.request.GET.get("filter")
        page = self.request.GET.get("page", 1)
        return get_search_results(query, filter, page)

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(**kwargs)
        context['result_types'] = [subclass.__name__ for subclass in Displayable.__subclasses__() if "pari" in subclass.__module__]
        context['filter'] = self.request.GET.get('filter')
        context['query'] = self.request.GET.get('query')
        return context
