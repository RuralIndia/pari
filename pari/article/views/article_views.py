from django.views.generic.detail import DetailView

from pari.article.models import Article


class ArticleDetail(DetailView):
    context_object_name = "blog_post"
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = context['blog_post']
        context['related_articles'] = article.related_posts.all()[:5]
        return context
