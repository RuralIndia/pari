from mezzanine.pages.page_processors import processor_for
from .models import Factoid
@processor_for("/")
def homepage_context(request, page):
    factoids=Factoid.objects.all()[:3].reverse()
    return{
        "factoids":factoids
    }

