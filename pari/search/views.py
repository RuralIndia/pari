from django.views.generic.list import ListView

from pari.article.common import get_result_types

from .models import get_search_results


class SearchList(ListView):
    context_object_name = "results"
    template_name = 'search/search_list.html'

    def get_queryset(self):
        query = self.request.GET.get("query")
        filter = self.request.GET.get("filter")
        page = self.request.GET.get("page", 1)
        return get_search_results(query, filter, page)

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(**kwargs)
        filter = self.request.GET.get('filter')
        context['filter'] = filter
        context['result_types'] = get_result_types(filter)
        context['query'] = self.request.GET.get('query')
        return context
