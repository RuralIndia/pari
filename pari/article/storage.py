import os
import StringIO
import boto
from django.core.files.storage import FileSystemStorage, default_storage
from mezzanine.conf import settings
from filebrowser_safe.storage import FileSystemStorageMixin
from boto.s3.key import Key
from urllib import quote

try:
    from PIL import Image, ImageFile, ImageOps, ImageDraw, ImageFont
except ImportError:
    import Image
    import ImageFile
    import ImageOps
    import ImageFont


class ParallelS3Storage(FileSystemStorage, FileSystemStorageMixin):
    def _save(self, name, content):
        if is_s3_storage():
            upload_to_s3(name, in_memory_file=content)
        return super(ParallelS3Storage, self)._save(name, content)


def is_s3_storage():
    return hasattr(settings, 'S3_URL') and settings.S3_URL is not None


def get_s3_bucket():
    conn = boto.connect_s3()
    return conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)


def get_s3_key(key):
    return "/media/%s" % key


def upload_to_s3(key, file_path=None, in_memory_file=None, string_io=None):
    bucket = get_s3_bucket()
    k = Key(bucket)
    k.key = get_s3_key(key)
    if file_path:
        k.set_contents_from_filename(file_path)
    elif in_memory_file:
        k.set_contents_from_string(in_memory_file.read())
    elif string_io:
        k.set_contents_from_string(string_io.getvalue())

    k.make_public()


def key_in_s3(key):
    bucket = get_s3_bucket()
    return Key(bucket, get_s3_key(key)).exists()


def get_s3_content(key, f):
    bucket = get_s3_bucket()
    Key(bucket, get_s3_key(key)).get_file(f)


def is_file_exists(path, url):
    if is_s3_storage():
        return key_in_s3(url)
    return os.path.exists(path)


def wrap_and_draw_centered_text(image_text, text_color, custom_font, image):
    image_width = image.size[0]
    image_height = image.size[1]

    def get_coordinates_for_centered_text(height, width):
        return (image_width - width) / 2, (image_height - height) / 2

    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(image_text, font=custom_font)
    initial_x, initial_y = get_coordinates_for_centered_text(height, width)
    if width + initial_x > image_width:
        y_offset = 0
        words_in_text = image_text.split(' ')
        space_between_lines = 2
        total_lines = len(words_in_text)
        total_words_height = (total_lines * height) + (space_between_lines * (total_lines - 2))
        for word in words_in_text:
            word_width, word_height = draw.textsize(word, font=custom_font)
            x, y = get_coordinates_for_centered_text(total_words_height, word_width)
            draw.text((x, y + y_offset), word, font=custom_font, fill=text_color)
            y_offset += word_height + space_between_lines
    else:
        draw.text((initial_x, initial_y), image_text, font=custom_font, fill=text_color)
    del draw


def create_new_image_with_text(image_path, image_text, quality=95, file_type='JPEG'):
    image_name = image_text.lower().replace(' ', '_') + "_alternate_image.jpg"
    image_path = os.path.join(image_path, image_name)
    s3_destination_url = "%s/%s" % (settings.THUMBNAILS_DIR_NAME, quote(image_name.encode("utf-8")))
    if not is_file_exists(image_path, s3_destination_url):
        image_width, image_height = (300, 300)
        image = Image.new('RGB', (image_width, image_height), (250, 250, 250))
        arial_font = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, 'open-sans', 'OpenSans-Light.ttf'), 30)
        text_color = (0, 0, 0)
        wrap_and_draw_centered_text(image_text.upper(), text_color, arial_font, image)
        save_image(file_type, image, image.info, quality, image_path, s3_destination_url)
    return os.path.join(settings.MEDIA_URL, image_name)


def save_image(file_type, image, image_info, quality, destination_path, s3_destination_url):
    if is_s3_storage():
        output_stream = StringIO.StringIO()
        image.save(output_stream, file_type, quality=quality, **image_info)
        upload_to_s3(s3_destination_url, string_io=output_stream)
    else:
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path))
        image.save(destination_path, file_type, quality=quality, **image_info)


def create_thumbnail(image_url, thumb_path, thumb_url, width, height, file_type, quality=95, mode='fit'):
    try:
        thumb_exists = is_file_exists(thumb_path, thumb_url)
    except UnicodeEncodeError:
        from mezzanine.core.exceptions import FileSystemEncodingChanged

        raise FileSystemEncodingChanged()

    if thumb_exists:
        return thumb_url

    if is_s3_storage():
        f = StringIO.StringIO()
        get_s3_content(image_url, f)
        f.seek(0)
    else:
        try:
            f = default_storage.open(image_url)
        except:
            return image_url

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
        if mode == 'fit':
            image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        else:
            image.thumbnail((width, height), Image.ANTIALIAS)

        save_image(file_type, image, image_info, quality, thumb_path, thumb_url)
    except Exception:
        try:
            os.remove(thumb_path)
        except Exception:
            pass
        return image_url

    return thumb_url
