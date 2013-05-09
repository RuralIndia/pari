from django.views.generic import DetailView, ListView
from pari.album.models import Album


class AlbumList(ListView):
    context_object_name = "albums"
    model = Album


class AlbumDetail(DetailView):
    context_object_name = "album"
    model = Album
