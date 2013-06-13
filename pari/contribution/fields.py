from itertools import chain

from django.forms import ChoiceField

from captcha.fields import ReCaptchaField

from pari.contribution.models import Contribution


class CaptchaField(ReCaptchaField):
    def __init__(self, *args, **kwargs):
        attrs = {'theme': 'white', 'width': '30'}
        super(CaptchaField, self).__init__(None, None, None, attrs, *args, **kwargs)


class ContributionsField(ChoiceField):
    def __init__(self, *args, **kwargs):
        choices = Contribution.objects.values_list('title')
        kwargs['choices'] = chain([("", "I want to..")], ((choice[0], choice[0]) for choice in choices))
        super(ContributionsField, self).__init__(*args, **kwargs)
