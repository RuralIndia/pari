import os

from django.db.models import get_models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage


from mezzanine.core.models import Displayable
from mezzanine.conf import settings

import boto
from boto.s3.key import Key

from .models import Article

try:
    from PIL import Image, ImageFile, ImageOps
except ImportError:
    import Image
    import ImageFile
    import ImageOps


def get_category_articles(category):
    return category.articles.filter(is_topic=False)


def get_location_articles(location):
    return Article.articles.filter(locations__location__contains=location.location)


def get_keyword_articles(keyword):
    return Article.articles.filter(keywords__keyword=keyword)


def get_author_articles(author):
    return Article.articles.filter(author=author)


def get_paginated_list(non_paginated, page):
    paginator = Paginator(non_paginated, 10)

    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated


def get_search_results(query, filter=None, page=1):
    if filter is not None:
        search_model = next(model for model in get_models() if issubclass(model, Displayable) and model.__name__==filter)
        results = search_model.objects.search(query)
    else:
        results = Displayable.objects.search(query)
    return get_paginated_list(results, page)


def get_article_list(article_queryset, page, filter):
    if filter is not None:
        article_queryset = article_queryset.filter(types__title__iexact=filter)

    return get_paginated_list(article_queryset, page)


def get_s3_bucket():
    conn = boto.connect_s3()
    return conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)


def get_s3_key(key):
    return "/media/%s" % key


def upload_to_s3(key, file_path=None, in_memory_file=None):
    bucket = get_s3_bucket()
    k = Key(bucket)
    k.key = get_s3_key(key)
    if file_path:
        k.set_contents_from_filename(file_path)
    elif in_memory_file:
        k.set_contents_from_string(in_memory_file.read())
    k.make_public()


def key_in_s3(key):
    bucket = get_s3_bucket()
    return bucket.get_key(get_s3_key(key)) is not None


def create_thumbnail(image_url, thumb_path, thumb_url, width, height, filetype, quality=95):
    f = default_storage.open(image_url)
    try:
        image = Image.open(f)
    except:
        return image_url

    image_info = image.info
    width = int(width)
    height = int(height)

    if width == image.size[0] and height == image.size[1]:
        return image_url

    if width == 0:
        width = image.size[0] * height / image.size[1]
    elif height == 0:
        height = image.size[1] * width / image.size[0]
    if image.mode not in ("P", "L", "RGBA"):
        image = image.convert("RGBA")

    # Required for progressive jpgs.
    ImageFile.MAXBLOCK = image.size[0] * image.size[1]

    try:
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        image = image.save(thumb_path, filetype, quality=quality, **image_info)
        if settings.S3_URL:
            upload_to_s3(thumb_url, file_path=thumb_path)
    except Exception:
        try:
            os.remove(thumb_path)
        except Exception:
            pass
        return image_url

    return thumb_url
