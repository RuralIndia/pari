from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

register_setting(
    name="SOCIAL_FACEBOOK",
    label=_("Facebook Page Url"),
    description="Facebook Page Url for PARI",
    editable=True,
    default="http://facebook.com",
)
register_setting(
    name="SOCIAL_TWITTER",
    label=_("Twitter Account"),
    description="Url to Twitter account",
    editable=True,
    default="http://twitter.com",
)
register_setting(
    name="SOCIAL_GOOGLE_PLUS",
    label=_("Google Plus Page Url"),
    description="Google Page Url for PARI",
    editable=True,
    default="http://plus.google.com",
)
register_setting(
    name="SOCIAL_GITHUB_REPO",
    label=_("Github Repo Url"),
    description="Github Url for PARI",
    editable=True,
    default="https://github.com/ruralindia/pari",
)
