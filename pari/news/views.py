from django.views.generic import DetailView, ListView, TemplateView
from pari.news.models import NewsPost, LatestArticle


class PariNewsView(TemplateView):
    template_name = "news/pari_news.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PariNewsView, self).get_context_data(*args, **kwargs)
        context['blog_post'] = NewsPost.objects.first()
        context['new_archive_articles'] = LatestArticle.objects.first().new_archive_articles.all()
        context['new_current_articles'] = LatestArticle.objects.first().new_current_articles.all()
        return context


class NewsPostDetail(DetailView):
    context_object_name = "blog_post"
    model = NewsPost


class NewsPostList(ListView):
    context_object_name = "blog_posts"
    model = NewsPost


class LatestArticleList(ListView):
    model = LatestArticle
