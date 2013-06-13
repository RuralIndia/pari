from django.views.generic import DetailView, ListView

from mezzanine.forms.page_processors import form_processor

from pari.article.templatetags.article_filters import get_page
from pari.contribution.models import Contribution


class ContributionList(ListView):
    context_object_name = "contributions"
    model = Contribution

    def get_context_data(self, **kwargs):
        context = super(ContributionList, self).get_context_data(**kwargs)
        contribute_form_page = get_page('ContributeForm')
        contribute_form = form_processor(self.request, contribute_form_page)
        context['contribute_form'] = contribute_form['form']
        context['contribute_form_page'] = contribute_form_page
        return context


class ContributionDetail(DetailView):
    context_object_name = "contribution"
    model = Contribution
