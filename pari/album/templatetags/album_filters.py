from django.template import Library

register = Library()


@register.filter
def get_file_path(image):
    return image.file.path


@register.filter
def all_images(album):
    return album.images.filter(is_cover=False).prefetch_related('location', 'photographer')
