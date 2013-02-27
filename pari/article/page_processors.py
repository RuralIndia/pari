from django.http import HttpResponseRedirect
from mezzanine.pages.page_processors import processor_for
from .models import Article

@processor_for("/")
def author_form(request, page):
    article_list = Article.articles.filter(featured_image__isnull=False)
    return {"article_list": article_list}