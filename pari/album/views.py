from django.views.generic import DetailView, ListView
from pari.album.models import Album, AlbumImage


class AlbumList(ListView):
    context_object_name = "albums"
    model = Album


class AlbumDetail(DetailView):
    context_object_name = "album"
    model = Album


class AlbumImageDetail(DetailView):
    context_object_name = "image"
    model = AlbumImage

    def get_object(self, queryset=None):
        return AlbumImage.objects.get(album__slug=self.kwargs['slug'],
                                      _order=int(self.kwargs['order']) - 1)
