from django.template import Context
from mezzanine.utils.views import render
from pari.album.models import Album


def index(request):
    albums = Album.objects.all()
    templates = ["album/index.html"]
    return render(request,templates, Context({"albums": albums}))


def show(request, slug):
    album = Album.objects.filter(slug=slug)
    templates = ["album/show.html"]
    return render(request, templates, Context({"album": album[0]}))
