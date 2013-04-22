from .admin import ArticleAdmin
from django.test import TestCase


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
