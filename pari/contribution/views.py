from django.views.generic import DetailView, ListView
from pari.contribution.models import Contribution


class ContributionList(ListView):
    context_object_name = "contributions"
    model = Contribution


class ContributionDetail(DetailView):
    context_object_name = "contribution"
    model = Contribution
