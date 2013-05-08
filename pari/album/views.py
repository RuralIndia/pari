from django.http import HttpResponse
from django.template import loader, Context
from pari.album.models import Album


def index(request):
    albums = Album.objects.all()
    template = loader.get_template("album/index.html")
    return HttpResponse(template.render(Context({"albums": albums})))