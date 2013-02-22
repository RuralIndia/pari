from django.template import Context

from mezzanine.utils.views import render


def index(request):
    templates = ["map/index.html"]
    c = Context()
    return render(request, templates, c)
