from django.template import Library
from datetime import date
from pari.faces.models import get_pinned_faces, get_pinned_face_images


register = Library()


@register.filter
def get_file_path(image):
    return image.image_collection_image.file.path


@register.filter
def get_group_image(grouped_faces):
    pinned_faces = get_pinned_faces(grouped_faces["list"][0].first_letter_of_district)
    if len(pinned_faces) != 0:
        return get_face_image(pinned_faces[0])
    else:
        return get_group_image_of_the_week(grouped_faces)


@register.filter
def get_face_image(face):
    face_images = get_pinned_face_images(face)
    if len(face_images) == 0:
        week_of_the_year = get_week_of_the_year()
        image_count = face.images.all().count()
        image_index = week_of_the_year % image_count
        return list(face.images.all())[image_index]
    else:
        return face_images[0]


@register.filter
def apply_pinning(face_images):
    pinned_face_images = list(face_images.filter(is_pinned=True))
    unpinned_face_images = list(face_images.filter(is_pinned=False))
    pinned_face_images.extend(unpinned_face_images)
    return pinned_face_images


@register.filter
def get_description(face_image):
    return face_image.description


@register.filter
def get_title(face_image):
    return face_image.title


def get_group_image_of_the_week(faces):
    district_of_the_week = get_district_of_the_week(faces)
    return get_face_image(district_of_the_week)


def get_district_of_the_week(faces):
    week_of_the_year = get_week_of_the_year()
    district_count = len(faces["list"])
    district_index = week_of_the_year % district_count
    return faces["list"][district_index]


def get_week_of_the_year():
    return date.today().isocalendar()[1]
