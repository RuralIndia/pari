from django.views.generic.detail import DetailView

from pari.article.models import Author, Article

class AuthorDetail(DetailView):
    context_object_name = "author"
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        author = context['author']
        context['filter'] = ""
        context['articles'] = Article.articles.filter(author=author)
        return context
