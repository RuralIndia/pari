from django.http import HttpResponseRedirect
from mezzanine.pages.page_processors import processor_for
from .models import Article

@processor_for("/")
def author_form(request, page):
    article_list = Article.articles.filter(featured_image__isnull=False)[:5]
    recent_articles = Article.articles.order_by('-publish_date')[:3]
    return {"article_list": article_list, "recent_articles": recent_articles}