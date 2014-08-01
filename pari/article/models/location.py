from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable
from mezzanine.core.fields import FileField
from mezzanine.utils.models import upload_to
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

from geoposition.fields import GeopositionField


class Location(Displayable):
    location = GeopositionField("Location")

    objects = DisplayableManager()
    search_fields = {"title": 10, "description": 5}

    image = FileField(verbose_name=_("Image"),
                      upload_to=upload_to("article.Location.image", "location"),
                      format="Image", max_length=255, null=True, blank=True)

    def get_as_latLng(self):
        return unicode(self.location).split(',')

    def get_articles(self):
        return self.article_set.filter(status=CONTENT_STATUS_PUBLISHED, is_topic=False)[:5]

    def get_topics(self):
        return self.article_set.filter(status=CONTENT_STATUS_PUBLISHED, is_topic=True)[:5]

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.location)

    @models.permalink
    def get_absolute_url(self):
        return ("location-detail", (), {"slug": unicode(self.slug)})

    class Meta:
        app_label = "article"

    @property
    def get_thumbnail(self):
        return self.image
