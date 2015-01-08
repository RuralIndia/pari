from mezzanine.boot.lazy_admin import LazyAdminSite
from django.core.cache import cache
from mezzanine.conf import settings

import requests
import re


class PariAdminSite(LazyAdminSite):
    def twitter_followers(self):
        followers = cache.get("twitter_followers")
        if not followers:
            followers = "- NA -"
            settings.use_editable()
            try:
                response = requests.get(
                    "https://twitter.com/" +
                    settings.SOCIAL_TWITTER.decode('utf-8'),
                    headers={"accept-language": "en-us, en; q=0.8"})
            except requests.RequestException:
                return followers
            if response.ok:
                content = response.content
                exists = re.search(r"followers_count(\S+?)(?P<number>\d+)", content)
                if exists:
                    followers = exists.group('number')
            expires_in_secs = settings.CACHE_MIDDLEWARE_SECONDS
            cache.set("twitter_followers", followers, expires_in_secs)
        return followers

    def facebook_likes(self):
        likes = cache.get("facebook_likes")
        if not likes:
            likes = "- NA -"
            settings.use_editable()
            if settings.SOCIAL_FACEBOOK_ID:
                try:
                    response = requests.get("https://graph.facebook.com/" +
                                            settings.SOCIAL_FACEBOOK_ID.decode('utf-8'))
                except requests.RequestException:
                    return likes
            if response.ok:
                likes = response.json()["likes"]
            expires_in_secs = settings.CACHE_MIDDLEWARE_SECONDS
            cache.set("facebook_likes", likes, expires_in_secs)
        return likes

    def index(self, request, extra_context=None):
        return super(PariAdminSite, self).index(request, extra_context={
            "twitter_followers": self.twitter_followers,
            "facebook_likes": self.facebook_likes
        })
