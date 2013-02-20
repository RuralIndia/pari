from .admin import ArticleAdmin
from django.test import TestCase


class ArticleAdminTestTest(TestCase):
    def test_includes_location_field(self):
        self.assertEqual(ArticleAdmin.fieldsets[0][1]['fields'][-2], 'location')
