from django.views.generic import DetailView, ListView
from pari.album.models import Album, AlbumImage, ImageCollectionImage


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


class ImageCollectionImageList(DetailView):
    context_object_name= "image_collection"
    model = ImageCollectionImage

    def get_object(self, queryset=None):
        album = Album.objects.get(slug=self.kwargs['slug'])
        return album.image_collection.images
