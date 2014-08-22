from django.views.generic import DetailView, ListView

from .models import Resource


class ResourceList(ListView):
    context_object_name = "resources"
    model = Resource


class ResourceDetail(DetailView):
    context_object_name = "resource"
    model = Resource


class ReportDetail(DetailView):
    context_object_name = "resource"
    model = Resource
    template_name = 'resources/report_detail.html'
