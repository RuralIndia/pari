from pyembed.core import consumer
from pyembed.core.error import PyEmbedError
from pyembed.core.discovery import DefaultDiscoverer, PyEmbedDiscoveryError
from pyembed.core.response import OEmbedLinkResponse
from pyembed.core import parse

import requests
import urlparse
import urllib

from HTMLParser import HTMLParser


class CustomDiscoverer(DefaultDiscoverer):
    def get_oembed_urls(self, url, oembed_format=None):
        response = requests.get(url)

        if not response.ok:
            raise PyEmbedDiscoveryError(
                'Failed to get %s (status code %s)' % (url, response.status_code))

        content_type = response.headers['content-type'].split(';')[0]
        if content_type in ["application/json", "text/xml", "application/xml"]:
            return [url]
        # Special case oembed
        if "soundcloud.com".find(url):
            oembed_format = "json"
            return super(CustomDiscoverer, self).get_oembed_urls(url, oembed_format)


class OEmbedNewLinkResponse(OEmbedLinkResponse):
    def fields(self):
        return super(OEmbedNewLinkResponse, self).fields() + ['url']

# Monkey-patch the RESPONSE CLASSES
parse.RESPONSE_CLASSES["link"] = OEmbedNewLinkResponse


def oembed_discover(url):
    oembed_data = {}
    if not url:
        return oembed_data, None
    try:
        oembed_urls = CustomDiscoverer().get_oembed_urls(url)
        oembed_response = consumer.get_first_oembed_response(oembed_urls)
    except (PyEmbedDiscoveryError, PyEmbedError), ex:
        return {}, unicode(ex)
    except requests.RequestException:
        return {}, "Invalid/Malform URL"
    for field in oembed_response.fields():
        oembed_data[field] = getattr(oembed_response, field)
        if oembed_response.type == "link":
            thumbnail = oembed_response.title
            if oembed_response.thumbnail_url:
                thumbnail = ('<img src="{0}" '
                             'alt={1}>').format(oembed_response.thumbnail_url,
                                                oembed_response.title)
            link_url = oembed_response.url or url
            oembed_data["html"] = ('<a href="{0}" '
                                   'target="_blank">{1}</a>').format(link_url,
                                                                     thumbnail)
    oembed_data = process_oembed_data(oembed_data)
    return oembed_data, None


class YTIframeParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        tag_attr_dict = dict(attrs)
        parts = urlparse.urlsplit(tag_attr_dict["src"])
        url_attrs = dict(urlparse.parse_qsl(parts.query))
        url_attrs["controls"] = "1"
        url_attrs["showinfo"] = "0"
        url_attrs["rel"] = "0"
        url_attrs["autohide"] = "1"
        url_attrs["modestbranding"] = "1"
        # Enable captions
        url_attrs["cc_load_policy"] = "1"
        src_url = urlparse.urlunsplit((parts.scheme, parts.netloc,
                                       parts.path, urllib.urlencode(url_attrs),
                                       parts.fragment))
        tag_attr_dict["src"] = src_url
        attr_str = ""
        for (key, val) in tag_attr_dict.iteritems():
            attr_str += " {0}".format(key)
            if val:
                attr_str += "=\"{0}\"".format(val)
        self.yt_url = "<iframe{0}></iframe>".format(attr_str)


def process_oembed_data(oembed_data):
    if oembed_data.get("provider_name") and oembed_data["provider_name"].lower() == "youtube":
        iframe_tag = oembed_data["html"]
        ytp = YTIframeParser()
        ytp.feed(iframe_tag)
        oembed_data["html"] = ytp.yt_url
    return oembed_data
