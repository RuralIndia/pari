from django.views.generic import ListView
from pari.faces.models import Face
from pari.faces.models import get_faces_by_first_letter


class FaceList(ListView):
    context_object_name = "faces"
    queryset = Face.objects.extra(select={'upper_district': 'upper(district)'}).order_by('upper_district')


class FaceDetail(ListView):
    context_object_name = "faces"
    model = Face

    def get_queryset(self):
        alphabet = self.kwargs['alphabet']
        return get_faces_by_first_letter(alphabet)


class FaceImageDetail(ListView):
    context_object_name = "faces"
    model = Face
