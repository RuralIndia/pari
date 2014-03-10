from pari.article.forms import DisplayableForm
from pari.faces.models import Face


class FaceForm(DisplayableForm):
    class Meta:
        model = Face
