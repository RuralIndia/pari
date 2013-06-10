from pari.article.forms import DisplayableForm
from pari.contribution.models import Contribution


class ContributionForm(DisplayableForm):
    def __init__(self, *args, **kwargs):
        super(ContributionForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 10

    class Meta:
        model = Contribution
