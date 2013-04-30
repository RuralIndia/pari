from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from mezzanine.accounts.models import User

import factory
from geoposition import Geoposition

from .admin import ArticleAdmin
from .models import Article, Location, Type, Category


class LocationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Location

    title = 'Location 1'
    location = Geoposition(1.2, 2.1)

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for article in extracted:
                self.article_set.add(article)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'User %s' % n)


class TypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Type

    title = 'Video'


class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category

    title = factory.Sequence(lambda n: 'Category %s' % n)

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for article in extracted:
                self.articles.add(article)


class ArticleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Article

    title = factory.Sequence(lambda n: 'Article %s' % n)
    location = factory.SubFactory(LocationFactory)
    user = factory.SubFactory(UserFactory)


class ArticleAdminTests(TestCase):
    def test_includes_location_field(self):
        self.assertIn("location", ArticleAdmin.fieldsets[0][1]['fields'])

    def test_includes_is_topic_field(self):
        self.assertIn("is_topic", ArticleAdmin.fieldsets[0][1]['fields'])

    def test_include_is_topic_in_list_display(self):
        self.assertIn("is_topic", ArticleAdmin.list_display)

    def test_includes_category_list_field(self):
        self.assertIn("category_list", ArticleAdmin.fieldsets[0][1]['fields'])

    def test_does_not_incluced_categories_from_BlogPost(self):
        self.assertNotIn("categories", ArticleAdmin.fieldsets[0][1]['fields'])

    def test_includes_article_type(self):
        self.assertIn("types", ArticleAdmin.fieldsets[0][1]['fields'])


class ArticleTests(TestCase):
    def setUp(self):
        self.video_article = ArticleFactory.create()
        self.video_article.types.add(TypeFactory.create())

    def test_is_video_article(self):
        self.assertTrue(self.video_article.is_video_article)


class LocationTests(TestCase):
    def setUp(self):
        self.location = LocationFactory.create()

    def test_get_as_latLng(self):
        self.assertEqual([u'1.2', u'2.1'], self.location.get_as_latLng())

    def test_get_articles_for_location_with_no_articles(self):
        location = LocationFactory()
        self.assertEqual(0, len(location.get_articles()))

    def test_get_articles_for_location_with_only_articles(self):
        location = LocationFactory(articles=(ArticleFactory(), ArticleFactory(), ArticleFactory()))
        self.assertEqual(3, len(location.get_articles()))

    def test_get_articles_for_location_with_topic_and_articles(self):
        location = LocationFactory(articles=(ArticleFactory(), ArticleFactory(), ArticleFactory(is_topic=True)))
        self.assertEqual(2, len(location.get_articles()))

    def test_get_topics_for_location_with_topic_and_articles(self):
        location = LocationFactory(articles=(ArticleFactory(), ArticleFactory(), ArticleFactory(is_topic=True)))
        self.assertEqual(1, len(location.get_topics()))


class ArticleViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_article_detail_view_context(self):
        article = ArticleFactory()
        response = self.client.get(reverse('article-detail', args=(article.slug,)))
        self.assertEqual(response.context['blog_post'], article)

    def test_article_detail_view(self):
        article = ArticleFactory()
        response = self.client.get(reverse('article-detail', args=(article.slug,)))
        self.assertContains(response, article.title, status_code=200)

    def test_category_detail_context(self):
        category = CategoryFactory(articles=(ArticleFactory(), ArticleFactory()))
        response = self.client.get(reverse('category-detail', args=(category.slug,)))
        self.assertEqual(2, len(response.context['articles']))

    def test_category_detail_context_not_include_topics(self):
        category = CategoryFactory(articles=(ArticleFactory(), ArticleFactory(is_topic=True)))
        response = self.client.get(reverse('category-detail', args=(category.slug,)))
        self.assertEqual(1, len(response.context['articles']))

    def test_search_results_contain_topics(self):
        topic = ArticleFactory()
        topic.is_topic = True
        response = self.client.get(reverse('search-detail'), {'q': 'article'})
        self.assertContains(response, topic, status_code=200)

    def test_search_results_should_contain_locations(self):
        location = LocationFactory()
        response = self.client.get(reverse('search-detail'), {'q': 'location'})
        self.assertContains(response, location, status_code=200)

    def test_search_page_contains_all_result_types(self):
        response = self.client.get(reverse('search-detail'), {'q': 'article'})
        self.assertContains(response.context['result_types'], ["Article"])

    def test_search_page_contains_all_result_types(self):
        response = self.client.get(reverse('search-detail'), {'q': 'article'})
        self.assertEqual(3, len(response.context['result_types']))

    def test_search_page_contains_all_result_types(self):
        response = self.client.get(reverse('search-detail'), {'q': 'article'})
        self.assertEqual(3, len(response.context['result_types']))