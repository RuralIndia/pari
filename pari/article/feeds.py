from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Article
from ..album.models import Album
from ..faces.models import Face
from ..resources.models import Resource, Factoid
from ..news.models import NewsPost

import itertools
import datetime


class AllFeed(Feed):
    title = "PARI consolidated feed"
    link  = "/feeds/all/"
    description = "Updates on the PARI site over the past 30 days"

    def items(self):
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        return itertools.chain(
            Article.objects.filter(publish_date__gte=thirty_days_ago),
            Album.objects.filter(publish_date__gte=thirty_days_ago),
            Face.objects.filter(publish_date__gte=thirty_days_ago),
            Resource.objects.filter(publish_date__gte=thirty_days_ago),
            Factoid.objects.filter(publish_date__gte=thirty_days_ago),
            NewsPost.objects.filter(publish_date__gte=thirty_days_ago)
        )


class ArticleFeed(Feed):
    title = "PARI article feed"
    link  = "/feeds/articles/"
    description = "Article updates on the PARI site over the past 30 days"

    def items(self):
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        return Article.objects.filter(publish_date__gte=thirty_days_ago)


class AlbumFeed(Feed):
    title = "PARI album feed"
    link  = "/feeds/albums/"
    description = "Album updates on the PARI site over the past 30 days"

    def items(self):
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        return Album.objects.filter(publish_date__gte=thirty_days_ago)


class FaceFeed(Feed):
    title = "PARI face feed"
    link  = "/feeds/faces/"
    description = "Face updates on the PARI site over the past 30 days"

    def items(self):
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        return Face.objects.filter(publish_date__gte=thirty_days_ago)


class ResourceFeed(Feed):
    title = "PARI resource feed"
    link  = "/feeds/resources/"
    description = "Resource updates on the PARI site over the past 30 days"

    def items(self):
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        return Resource.objects.filter(publish_date__gte=thirty_days_ago)


class FactoidFeed(Feed):
    title = "PARI factoid feed"
    link  = "/feeds/factoids/"
    description = "Factoid updates on the PARI site over the past 30 days"

    def items(self):
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        return Factoid.objects.filter(publish_date__gte=thirty_days_ago)


class NewsPostFeed(Feed):
    title = "PARI news feed"
    link  = "/feeds/newsposts/"
    description = "News updates on the PARI site over the past 30 days"

    def items(self):
        thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
        return NewsPost.objects.filter(publish_date__gte=thirty_days_ago)
