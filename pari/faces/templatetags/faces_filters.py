from django.template import Library
from datetime import date

register = Library()


@register.filter
def get_file_path(image):
    return image.image_collection_image.file.path


@register.filter
def get_thumbnail_of_the_week(faces):
    district_of_the_week = get_district_of_the_week(faces)
    return get_face_of_the_week(district_of_the_week)


@register.filter
def get_face_of_the_week(face):
    week_of_the_year = get_week_of_the_year()
    image_count = face.images.count()
    image_index = week_of_the_year % image_count
    return list(face.images.all())[image_index]

@register.filter
def get_description(face_image):
    return face_image.description


def get_district_of_the_week(faces):
    week_of_the_year = get_week_of_the_year()
    district_count = len(faces)
    district_index = week_of_the_year % district_count
    return faces["list"][district_index]


def get_week_of_the_year():
    return date.today().isocalendar()[1];


