from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.utils import timezone
from django.shortcuts import render

from mezzanine.conf import settings

from .models import Article
from ..album.models import Album
from ..faces.models import Face
from ..resources.models import Resource, Factoid
from ..news.models import NewsPost

import itertools
import datetime


class BaseFeed(Feed):
    def __init__(self, *args, **kwargs):
        self.days_ago = int(settings.FEED_GENERATION_DAYS)
        super(BaseFeed, self).__init__(*args, **kwargs)

    def __call__(self, request, *args, **kwargs):
        feed_format = request.GET.get("format")
        if feed_format:
            if feed_format == "atom":
                self.feed_type = Atom1Feed
            else:
                self.feed_type = Rss201rev2Feed
        else:
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
    link = "/feeds/all/"

    def __init__(self, *args, **kwargs):
        super(AllFeed, self).__init__(*args, **kwargs)
        self.description = ("Updates on the PARI site over the "
                            "past {0} days".format(self.days_ago))

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=self.days_ago)
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
    link = "/feeds/articles/"

    def __init__(self, *args, **kwargs):
        super(ArticleFeed, self).__init__(*args, **kwargs)
        self.description = ("Article updates on the PARI site "
                            "over the past {0} days".format(self.days_ago))

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=self.days_ago)
        return Article.objects.filter(publish_date__gte=x_days_ago)


class AlbumFeed(BaseFeed):
    title = "PARI album feed"
    link = "/feeds/albums/"

    def __init__(self, *args, **kwargs):
        super(AlbumFeed, self).__init__(*args, **kwargs)
        self.description = ("Album updates on the PARI site "
                            "over the past {0} days".format(self.days_ago))

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=self.days_ago)
        return Album.objects.filter(publish_date__gte=x_days_ago)


class FaceFeed(BaseFeed):
    title = "PARI face feed"
    link = "/feeds/faces/"

    def __init__(self, *args, **kwargs):
        super(FaceFeed, self).__init__(*args, **kwargs)
        self.description = ("Face updates on the PARI site "
                            "over the past {0} days".format(self.days_ago))

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=self.days_ago)
        return Face.objects.filter(publish_date__gte=x_days_ago)


class ResourceFeed(BaseFeed):
    title = "PARI resource feed"
    link = "/feeds/resources/"

    def __init__(self, *args, **kwargs):
        super(ResourceFeed, self).__init__(*args, **kwargs)
        self.description = ("Resource updates on the PARI site over the "
                            "past {0} days".format(self.days_ago))

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=self.days_ago)
        return Resource.objects.filter(publish_date__gte=x_days_ago)


class FactoidFeed(BaseFeed):
    title = "PARI factoid feed"
    link = "/feeds/factoids/"

    def __init__(self, *args, **kwargs):
        super(FactoidFeed, self).__init__(*args, **kwargs)
        self.description = ("Factoid updates on the PARI site over the "
                            "past {0} days".format(self.days_ago))

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=self.days_ago)
        return Factoid.objects.filter(publish_date__gte=x_days_ago)


class NewsPostFeed(BaseFeed):
    title = "PARI news feed"
    link = "/feeds/newsposts/"

    def __init__(self, *args, **kwargs):
        super(NewsPostFeed, self).__init__(*args, **kwargs)
        self.description = ("News updates on the PARI site over the "
                            "past {0} days".format(self.days_ago))

    def items(self):
        x_days_ago = timezone.now() - datetime.timedelta(days=self.days_ago)
        return NewsPost.objects.filter(publish_date__gte=x_days_ago)


def feeds_list_page(request):
    return render(request, "feeds/feeds_list.html", {})
