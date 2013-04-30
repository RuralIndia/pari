from django.db import models


class Type(models.Model):
    title = models.CharField(max_length=5)
    icon_class = models.CharField(max_length=20)

    def __str__(self):
        return "%s" % (self.title)

    def __unicode__(self):
        return "%s" % (self.title)

    class Meta:
        app_label = "article"
