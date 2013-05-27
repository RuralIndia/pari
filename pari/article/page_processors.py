from django.utils import timezone

from mezzanine.pages.page_processors import processor_for
from .models import Article, Category


@processor_for("/")
def homepage_context(request, page):
    article_list = Article.articles.filter(featured_image__isnull=False)[:5]
    categories = Category.objects.all()
    recent_articles = Article.articles.order_by('-publish_date')[:6]
    start_time, end_time = get_archive_range()
    return {
        "article_list": article_list,
        "recent_articles": recent_articles,
        "categories": categories,
        "start_time": start_time,
        "end_time": end_time
    }


def get_archive_range():
    start_time = Article.objects.all().order_by('publish_date')[0].publish_date
    end_time = timezone.now()
    return start_time, end_time
