from django.views.generic import ListView
from pari.faces.models import Face, get_face_images_by_district_first_letter


class FaceList(ListView):
    context_object_name = "faces"
    queryset = Face.objects.filter(district__district__isnull=False).extra(select={'upper_district': 'upper(district)'}).order_by('upper_district')


class FaceDetail(ListView):
    context_object_name = "face_images"
    model = Face

    def get_queryset(self):
        alphabet = self.kwargs['alphabet']
        return get_face_images_by_district_first_letter(alphabet)


class FaceImageDetail(ListView):
    context_object_name = "faces"
    model = Face
