from django.views.generic import DetailView, ListView
from pari.album.models import Album, AlbumImage, ImageCollectionImage


class AlbumList(ListView):
    model = Album

    def get_context_data(self, *args, **kwargs):
        context = super(AlbumList, self).get_context_data(*args, **kwargs)
        context['albums'] = self.kwargs['albums']()
        return context


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
