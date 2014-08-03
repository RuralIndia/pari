from django.views.generic import DetailView, ListView
from pari.news.models import NewsPost, LatestArticle


class NewsPostDetail(DetailView):
    context_object_name = "blog_post"
    model = NewsPost


class NewsPostList(ListView):
    context_object_name = "blog_posts"
    model = NewsPost


class LatestArticleList(ListView):
    model = LatestArticle
