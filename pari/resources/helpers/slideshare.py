import urllib
import requests
import json
from requests import Timeout, ConnectionError, HTTPError

SLIDESHARE_OEMBED_ENDPOINT = "http://www.slideshare.net/api/oembed/2"
SLIDESHARE_SLIDESHOW_URL = "http://www.slideshare.net/slideshow/embed_code/%s&format=json"


def get_resource_thumb_url(embed_code):
    thumb_url = None
    try:
        urlvalue = urllib.unquote(SLIDESHARE_SLIDESHOW_URL % embed_code)
        payload = {'url': urlvalue}
        response = requests.get(SLIDESHARE_OEMBED_ENDPOINT, params=payload, timeout=10)
        response_dict = json.loads(response.text)
        thumb_url = response_dict.get('thumbnail')
    except (Timeout, ConnectionError, HTTPError, ValueError):
        pass

    return thumb_url or ''
