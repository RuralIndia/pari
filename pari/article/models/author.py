from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Displayable
from mezzanine.core.managers import DisplayableManager
from mezzanine.core.fields import FileField


class Author(Displayable):
    email = models.EmailField(null=True, blank=True)
    twitter_username = models.CharField(max_length=50, null=True, blank=True)
    facebook_username = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    image = FileField(verbose_name=_("Author's Image"), format="Image", max_length=255, null=True, blank=True)
    objects = DisplayableManager()

    class Meta:
        app_label = "article"

    @models.permalink
    def get_absolute_url(self):
        return ("author-detail", (), {"slug": unicode(self.slug)})

    @property
    def get_thumbnail(self):
        return self.image
