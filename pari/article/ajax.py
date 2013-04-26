from django.template.loader import render_to_string

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from .models import Category, Type, Location
from .views import get_article_list


@dajaxice_register
def category_article_filter(request, category, filter=None, page=1):
    category = Category.objects.get(pk=category)
    article_queryset = category.articles.all()

    return article_filter(article_queryset, category.title, filter, page)
    

@dajaxice_register
def location_article_filter(request, location, filter=None, page=1):
    location = Location.objects.get(pk=location)
    article_queryset = location.article_set.all()

    return article_filter(article_queryset, location.title, filter, page)


def article_filter(article_queryset, title, filter, page):
    if(filter is not None):
        article_queryset = article_queryset.filter(types__title__iexact=filter)

    articles = get_article_list(article_queryset, page)
    render = render_to_string('article/includes/article_list.html', {'articles': articles,
                                                                     'title': title,
                                                                     'filter': filter,
                                                                     'types': Type.objects.all()})

    dajax = Dajax()
    dajax.assign('#article-list', 'innerHTML', render)
    dajax.script('ArticleFilter.init();')
    return dajax.json()


