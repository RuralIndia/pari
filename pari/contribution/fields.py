from captcha.fields import ReCaptchaField


class CaptchaField(ReCaptchaField):
    def __init__(self, *args, **kwargs):
        attrs = {'theme': 'clean', 'width': '30'}
        super(CaptchaField, self).__init__(None, None, None, attrs, *args, **kwargs)
