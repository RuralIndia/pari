import os
from urllib import quote, unquote

from django.core.files.storage import default_storage
from django.template.loader import render_to_string

from mezzanine.conf import settings
from mezzanine import template

from .article_filters import get_type
from pari.article.common import key_in_s3, create_thumbnail


register = template.Library()


@register.inclusion_tag("article/includes/list_media.html")
def list_media_for(article, width, height):
    return {'article': article,
            'width': width,
            'height': height,
            }


@register.inclusion_tag("article/includes/featured_content.html")
def featured_content_for(article):
    return {'article': article}


@register.inclusion_tag("article/includes/article_list.html", takes_context=True)
def article_list(context, title=None):
    return {'articles': context['articles'],
            'title': title,
            'types': context['types'],
            'filter': context['filter'],
            'request': context['request']}


@register.simple_tag(takes_context=True)
def display_result(context):
    return render_to_string("article/includes/%s_atom.html" % get_type(context['result']),
                            {'result': context['result'], 'request': context['request']})


@register.inclusion_tag("article/includes/search_result_list.html", takes_context=True)
def render_results(context):
    return {'results': context['results'],
            'query': context['query'],
            'result_types': context['result_types'],
            'filter': context['filter'],
            'request': context['request']}


@register.inclusion_tag("article/includes/paginator.html")
def paginate_list(results, page=1):
    return {'results': results, 'page': page}


@register.inclusion_tag("article/includes/share.html")
def render_share_widgets(title, url):
    return {'url': url, 'title': title}


@register.simple_tag
def thumbnail(image_url, width, height, quality=95):
    """
    Given the URL to an image, resizes the image using the given width and
    height on the first time it is requested, and returns the URL to the new
    resized image. if width or height are zero then original ratio is
    maintained.
    """
    if not image_url:
        image_url = "no_image.jpg"

    image_url = unquote(unicode(image_url))
    if image_url.startswith(settings.MEDIA_URL):
        image_url = image_url.replace(settings.MEDIA_URL, "", 1)
    image_dir, image_name = os.path.split(image_url)
    image_prefix, image_ext = os.path.splitext(image_name)
    filetype = {".png": "PNG", ".gif": "GIF"}.get(image_ext, "JPEG")
    thumb_name = "%s-%sx%s%s" % (image_prefix, width, height, image_ext)
    thumb_dir = os.path.join(settings.MEDIA_ROOT, image_dir,
                             settings.THUMBNAILS_DIR_NAME)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_path = os.path.join(thumb_dir, thumb_name)
    thumb_url = "%s/%s" % (settings.THUMBNAILS_DIR_NAME,
                           quote(thumb_name.encode("utf-8")))
    image_url_path = os.path.dirname(image_url)
    if image_url_path:
        thumb_url = "%s/%s" % (image_url_path, thumb_url)

    if settings.S3_URL:
        if key_in_s3(thumb_url):
            return thumb_url

    try:
        thumb_exists = os.path.exists(thumb_path)
    except UnicodeEncodeError:
        # The image that was saved to a filesystem with utf-8 support,
        # but somehow the locale has changed and the filesystem does not
        # support utf-8.
        from mezzanine.core.exceptions import FileSystemEncodingChanged
        raise FileSystemEncodingChanged()
    if thumb_exists:
        # Thumbnail exists, don't generate it.
        return thumb_url
    elif not default_storage.exists(image_url):
        # Requested image does not exist, just return its URL.
        return image_url

    return create_thumbnail(image_url, thumb_path, thumb_url, width, height, filetype)
