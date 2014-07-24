from django.utils import timezone

from mezzanine.pages.page_processors import processor_for
from .models import Article, Category


@processor_for("/")
def homepage_context(request, page):
    article_list = Article.articles.prefetch_related('locations')\
                        .filter(pin_to_home=True)\
                        .exclude(featured_image__isnull=True)\
                        .exclude(featured_image='')\
                        .order_by('-updated')[:10]
    categories = Category.objects.all()[:9]
    recent_articles = Article.articles.prefetch_related('locations').order_by('-publish_date')[:6]
    start_time, end_time = get_archive_range()
    return {
        "article_list": article_list,
        "recent_articles": recent_articles,
        "categories": categories,
        "start_time": start_time,
        "end_time": end_time
    }


def get_archive_range():
    end_time = timezone.now()

    try:
        start_time = Article.articles.order_by('publish_date')[0].publish_date
    except IndexError:
        start_time = end_time

    return start_time, end_time
