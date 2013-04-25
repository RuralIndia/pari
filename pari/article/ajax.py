from django.template.loader import render_to_string

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from .models import Category, Type
from .views import get_article_list


@dajaxice_register
def category_article_filter(request, category, filter, page=1):
    category = Category.objects.get(pk=category)
    articles = get_article_list(category.articles.filter(types__title__iexact=filter), 1)
    render = render_to_string('article/includes/article_list.html', {'articles': articles,
                                                                     'title': category.title,
                                                                     'filter': filter,
                                                                     'types': Type.objects.all()})

    dajax = Dajax()
    dajax.assign('#article-list', 'innerHTML', render)
    dajax.script('ArticleFilter.init();')
    return dajax.json()
