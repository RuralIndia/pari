import factory
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .models import NewsPost
from ..article.tests import UserFactory


class NewsPostFactory(factory.DjangoModelFactory):
    FACTORY_FOR = NewsPost

    title = factory.Sequence(lambda n: 'News post %s' % n)
    user = factory.SubFactory(UserFactory)
    content = "<div>News post content</div>"


class PariNewsViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pari_news_view_gets_the_latest_news_post(self):
        NewsPostFactory.create(title='news1')
        NewsPostFactory.create(title='news2')
        news3 = NewsPostFactory.create(title='news3')

        response = self.client.get(reverse('pari-news'))
        self.assertEqual(response.context['blog_post'], news3)
