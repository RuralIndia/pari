from django.template import Library
from datetime import date
from pari.faces.models import get_pinned_face, get_pinned_face_image


register = Library()


@register.filter
def get_file_path(image):
    return image.image_collection_image.file.path

@register.filter
def get_group_image(grouped_faces):
    pinned_face = get_pinned_face(grouped_faces["list"][0].first_letter_of_district)
    if len(pinned_face) != 0:
        return get_face_image(pinned_face[0])
    else:
        return get_group_image_of_the_week(grouped_faces)

@register.filter
def get_face_image(face):
    face_image = get_pinned_face_image(face)
    if len(face_image) == 0:
        week_of_the_year = get_week_of_the_year()
        image_count = face.images.count()
        image_index = week_of_the_year % image_count
        return list(face.images.all())[image_index]
    else:
        return face_image[0]

@register.filter
def get_description(face_image):
    return face_image.description


def get_group_image_of_the_week(faces):
    district_of_the_week = get_district_of_the_week(faces)
    return get_face_image(district_of_the_week)


def get_district_of_the_week(faces):
    week_of_the_year = get_week_of_the_year()
    district_count = len(faces)
    district_index = week_of_the_year % district_count
    return faces["list"][district_index]


def get_week_of_the_year():
    return date.today().isocalendar()[1];


