from django.views.generic import DetailView, ListView

from mezzanine.forms.page_processors import form_processor

from pari.article.templatetags.article_filters import get_page
from pari.contribution.forms import CaptchaForm
from pari.contribution.models import Contribution


class ContributionList(ListView):
    context_object_name = "contributions"
    model = Contribution

    def get_context_data(self, **kwargs):
        context = super(ContributionList, self).get_context_data(**kwargs)
        contact_us_page = get_page('Contact Us')
        contact_us_form = form_processor(self.request, contact_us_page)
        context['contact_us_form'] = contact_us_form['form']
        context['contact_us_page'] = contact_us_page
        captcha_form = CaptchaForm()
        contact_us_form['form'].fields['field_4'] = captcha_form.fields.get('captcha')
        return context


class ContributionDetail(DetailView):
    context_object_name = "contribution"
    model = Contribution
