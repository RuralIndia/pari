import os
from lxml import html
from lxml.etree import tostring

from pari.article.templatetags import article_tags
from mezzanine.conf import settings


def article_content_filter(content):
    html_content = html.fromstring(content)
    images = html_content.cssselect('img')
    for image in images:
        image_source = image.attrib['src']
        if image_source.startswith("/"):
            image_width = image.attrib.get('width')
            image_height = image.attrib.get('height')
            if image_width or image_height:
                image_thumbnail_source = os.path.join(settings.MEDIA_URL, article_tags.thumbnail(image_source, image_width, image_height))
                image.attrib['src'] = image_thumbnail_source

    return tostring(html_content)
