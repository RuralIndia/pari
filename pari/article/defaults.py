from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name="SITE_FULL_TITLE",
    label=_("Full Site Title"),
    description="Expanded title",
    editable=True,
    default="People's Archive of Rural India",
)
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
register_setting(
    name="SOCIAL_PINTEREST",
    label=_("Pintereset Url"),
    description="Pinterest Url",
    editable=True,
    default="https://www.pinterest.com",
)
register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=(
        "SITE_FULL_TITLE",
    ),
    append=True,
)
register_setting(
    name="ALLOW_COMMENTS_IN_TALKING_ALBUM",
    label=_("Allow comments in talking albums"),
    description="Check to enable comments section for talking albums",
    editable=True,
    default=False
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_1_HEADING",
    label=_("Blurb section-1 heading"),
    description="A blurb heading that will appear in the first portion of layout allocated for the blurb texts below the carousel",
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_1_CONTENT",
    label=_("Blurb section-1 content"),
    description="A blurb message corresponding to the blurb heading",
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_1_URL",
    label=_("Blurb section-1 URL"),
    description="A blurb URL corresponding to the blurb heading, the URL has to be relative, (e.g) /resources ",
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_2_HEADING",
    label=_("Blurb section-2 heading"),
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_2_CONTENT",
    label=_("Blurb section-2 content"),
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_2_URL",
    label=_("Blurb section-2 URL"),
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_3_HEADING",
    label=_("Blurb section-3 heading"),
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_3_CONTENT",
    label=_("Blurb section-3 content"),
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_3_URL",
    label=_("Blurb section-3 URL"),
    editable=True,
    default=""
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_4_HEADING",
    label=_("Blurb section-4 heading"),
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_4_CONTENT",
    label=_("Blurb section-4 content"),
    editable=True,
    default="",
)
register_setting(
    name="HOME PAGE_BLURB_SECTION_4_URL",
    label=_("Blurb section-4 URL"),
    editable=True,
    default=""
)
register_setting(
    name="FEED_GENERATION_DAYS",
    label=_("Number of days since from when feeds are generated"),
    editable=True,
    default=30
)
