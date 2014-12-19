from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.utils import timezone
from mezzanine.conf import settings

from .models import Article
from ..album.models import Album
from ..faces.models import Face
from ..resources.models import Resource, Factoid
from ..news.models import NewsPost

import itertools
import datetime

days_ago = int(settings.FEED_GENERATION_DAYS)


class BaseFeed(Feed):
    def __call__(self, request, *args, **kwargs):
        accept_header = request.META.get("HTTP_ACCEPT", "")
        if accept_header.find("application/atom+xml") >= 0:
            self.feed_type = Atom1Feed
        else:
            self.feed_type = Rss201rev2Feed
        return super(BaseFeed, self).__call__(request, *args, **kwargs)

    def item_pubdate(self, item):
        return item.publish_date

    def item_author_name(self, item):
        author = getattr(item, 'author', None)
        if author:
            return author.title
        user = getattr(item, 'user', None)
        if user:
            return item.user.get_full_name() or item.user.username

    def item_author_link(self, item):
        author = getattr(item, 'author', None)
        if author:
            return author.get_absolute_url()

class AllFeed(BaseFeed):
    title = "PARI consolidated feed"
    link  = "/feeds/all/"
    description = "Updates on the PARI site over the past {0} days".format(days_ago)

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=days_ago)
        return itertools.chain(
            Article.objects.filter(publish_date__gte=x_days_ago),
            Album.objects.filter(publish_date__gte=x_days_ago),
            Face.objects.filter(publish_date__gte=x_days_ago),
            Resource.objects.filter(publish_date__gte=x_days_ago),
            Factoid.objects.filter(publish_date__gte=x_days_ago),
            NewsPost.objects.filter(publish_date__gte=x_days_ago)
        )


class ArticleFeed(BaseFeed):
    title = "PARI article feed"
    link  = "/feeds/articles/"
    description = "Article updates on the PARI site over the past {0} days".format(days_ago)

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=days_ago)
        return Article.objects.filter(publish_date__gte=x_days_ago)


class AlbumFeed(BaseFeed):
    title = "PARI album feed"
    link  = "/feeds/albums/"
    description = "Album updates on the PARI site over the past {0} days".format(days_ago)

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=days_ago)
        return Album.objects.filter(publish_date__gte=x_days_ago)


class FaceFeed(BaseFeed):
    title = "PARI face feed"
    link  = "/feeds/faces/"
    description = "Face updates on the PARI site over the past {0} days".format(days_ago)

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=days_ago)
        return Face.objects.filter(publish_date__gte=x_days_ago)


class ResourceFeed(BaseFeed):
    title = "PARI resource feed"
    link  = "/feeds/resources/"
    description = "Resource updates on the PARI site over the past {0} days".format(days_ago)

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=days_ago)
        return Resource.objects.filter(publish_date__gte=x_days_ago)


class FactoidFeed(BaseFeed):
    title = "PARI factoid feed"
    link  = "/feeds/factoids/"
    description = "Factoid updates on the PARI site over the past {0} days".format(days_ago)

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=days_ago)
        return Factoid.objects.filter(publish_date__gte=x_days_ago)


class NewsPostFeed(BaseFeed):
    title = "PARI news feed"
    link  = "/feeds/newsposts/"
    description = "News updates on the PARI site over the past {0} days".format(days_ago)

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=days_ago)
        return NewsPost.objects.filter(publish_date__gte=x_days_ago)
