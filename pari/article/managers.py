from mezzanine.core.managers import DisplayableManager


class BlogManager(DisplayableManager):
    def get_query_set(self):
        return super(ArticleManager, self).get_query_set()


class ArticleManager(DisplayableManager):
    def get_query_set(self):
        return super(ArticleManager, self).get_query_set().filter(is_topic=False)


class TopicManager(DisplayableManager):
    def get_query_set(self):
        return super(TopicManager, self).get_query_set().filter(is_topic=True)
