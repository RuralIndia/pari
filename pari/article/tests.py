from django.test import TestCase

from mezzanine.accounts.models import User

import factory
from geoposition import Geoposition

from .admin import ArticleAdmin
from .models import Article, Location, Type


class LocationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Location

    title = 'Location 1'
    location = Geoposition(1.2, 2.1)


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user %s' % n)


class TypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Type

    title = 'Video'


class ArticleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Article

    title = 'article 1'
    location = factory.SubFactory(LocationFactory)
    user = factory.SubFactory(UserFactory)


class ArticleAdminTest(TestCase):
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


class ArticleTest(TestCase):
    def setUp(self):
        self.video_article = ArticleFactory.create()
        self.video_article.types.add(TypeFactory.create())

    def test_is_video_article(self):
        self.assertTrue(self.video_article.is_video_article)


class LocationTest(TestCase):
    def setUp(self):
        self.location = LocationFactory.create()

    def test_get_as_latLng(self):
        self.assertEqual([u'1.2', u'2.1'], self.location.get_as_latLng())
