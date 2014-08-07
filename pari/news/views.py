from django.views.generic import DetailView, ListView, TemplateView
from pari.news.models import NewsPost, LatestArticle, get_latest_news_post, get_chosen_archive_articles, \
    get_chosen_current_articles


class PariNewsView(TemplateView):
    template_name = "news/pari_news.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PariNewsView, self).get_context_data(*args, **kwargs)
        context['blog_post'] = get_latest_news_post()
        context['new_archive_articles'] = get_chosen_archive_articles()
        context['new_current_articles'] = get_chosen_current_articles()
        return context


class NewsPostDetail(DetailView):
    context_object_name = "blog_post"
    model = NewsPost


class NewsPostList(ListView):
    context_object_name = "blog_posts"
    model = NewsPost


class LatestArticleList(ListView):
    model = LatestArticle
