from django.template import Library

register = Library()


@register.filter
def get_file_path(image):
    return image.file.path
