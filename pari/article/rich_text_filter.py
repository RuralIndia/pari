import os
from lxml import html

from mezzanine.conf import settings
from pari.article.templatetags import article_tags


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

    return html.tostring(html_content).encode('utf8')
