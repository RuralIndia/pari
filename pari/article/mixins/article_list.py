from pari.article.ajax import get_article_list


class ArticleListMixin(object):
    article_list_context_name = "articles"

    def get_article_list(self):
        article_queryset = self.get_article_list_queryset()
        page = self.request.GET.get('page')
        filter = self.request.GET.get('filter')
        return get_article_list(article_queryset, page, filter)

    def get_context_data(self, **kwargs):
        context = super(ArticleListMixin, self).get_context_data(**kwargs)
        context[self.article_list_context_name] = self.get_article_list()
        return context
