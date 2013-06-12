from django.views.generic import DetailView, ListView
from itertools import chain
import random
from .models import Resource, Factoid


class ResourceList(ListView):
    context_object_name = "resources"
    model = Resource

    def get_context_data(self, **kwargs):
        context = super(ResourceList, self).get_context_data(**kwargs)
        context['resources'] = list(chain(Resource.objects.all().order_by('?')[:18], Factoid.objects.all().order_by('?')[:2]))
        random.shuffle(context['resources'])
        return context

class ResourceDetail(DetailView):
    context_object_name = "resource"
    model = Resource
