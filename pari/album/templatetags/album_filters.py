from django.template import Library

register = Library()


@register.filter
def get_file_path(album_image):
    return album_image.image_collection_image.file.path


@register.filter
def get_image_collection_image_path(image):
    return image.file.path


@register.filter
def all_images(album):
    return album.images.prefetch_related('location', 'photographer')
