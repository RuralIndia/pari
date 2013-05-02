from mezzanine.core.models import Displayable
from mezzanine.utils.views import render


def search_detail(request):
    query = request.GET.get("query")
    filter = request.GET.get("filter")
    results = Displayable.objects.search(query)
    if filter is not None:
        results = [result for result in results if filter == result.__class__.__name__]
    result_types = [subclass.__name__ for subclass in Displayable.__subclasses__() if "pari" in subclass.__module__]
    templates = [u"article/search_detail.html"]
    c = {"query": query, "results": results, "result_types": result_types, "filter": filter}
    return render(request, templates, c)
