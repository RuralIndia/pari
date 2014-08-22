from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from pari.resources.admin import ResourceAdmin
from pari.resources.models import Resource, Factoid
import factory


class ResourceAdminTest(TestCase):
    def test_includes_authors(self):
        self.assertIn("authors", ResourceAdmin.fieldsets[0][1]['fields'])

    def test_includes_focus(self):
        self.assertIn("focus", ResourceAdmin.fieldsets[0][1]['fields'])

    def test_includes_copyright(self):
        self.assertIn("copyright", ResourceAdmin.fieldsets[0][1]['fields'])


class FactoidFactory(TestCase):
    FACTORY_FOR = Factoid
    title = factory.Sequence(lambda n: 'Factoid %s' % n)


class ResourceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Resource
    title = factory.Sequence(lambda n: 'Resource %s' % n)
    description="Description"
    embed_source=factory.Sequence(lambda n: '2318 %s' % n)
    focus="<div>Focus</div>"
    copyright="<div>Copyright</div>"
    authors="<div>Authors</div>"


class ResourcesViewTest(TestCase):
        def setUp(self):
            self.client=Client()

        def test_resource_detail_view_context(self):
            resource=ResourceFactory()
            response = self.client.get(reverse('resource-detail', args=(resource.slug,)))
            self.assertEqual(response.context['resource'], resource)

        def test_resource_detail_view(self):
            resource = ResourceFactory()
            response = self.client.get(reverse('resource-detail', args=(resource.slug,)))
            self.assertContains(response, resource.title, status_code=200)
