from django.db import models


class Profile(models.Model):
    user = models.OneToOneField("auth.User")
    address = models.TextField(null=True, max_length=200)
