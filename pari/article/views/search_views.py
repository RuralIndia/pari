from mezzanine.core.models import Displayable
from mezzanine.utils.views import render


def search_detail(request):
    query = request.GET.get("q", "")
    articles = Displayable.objects.search(query)
    result_types = [subclass.__name__ for subclass in Displayable.__subclasses__() if "pari" in subclass.__module__]
    templates = [u"article/search_detail.html"]
    c = {"query": query, "articles": articles, "result_types": result_types}
    return render(request, templates, c)
