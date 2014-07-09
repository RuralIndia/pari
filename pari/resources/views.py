from itertools import chain
import random

from django.views.generic import DetailView, ListView

from .models import Resource, Factoid
class ResourceList(ListView):
    context_object_name = "resources"
    template_name = "resources/resource_list.html"

    def get_queryset(self):
        resources = Resource.objects.all()[:16]
        factoids = Factoid.objects.all()[:4]
        entries = list(chain(resources, factoids))
        random.shuffle(entries)
        return entries


class ResourceDetail(DetailView):
    context_object_name = "resource"
    model = Resource
