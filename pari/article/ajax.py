from django.template.loader import render_to_string

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from .models import Article


@dajaxice_register
def category_article_filter(request, category):
    articles = Article.objects.filter(pk=id)
    render = render_to_string('article/includes/article_list.html', {'articles': articles})

    dajax = Dajax()
    dajax.assign('#article-list', 'innerHTML', render)
    return dajax.json()
