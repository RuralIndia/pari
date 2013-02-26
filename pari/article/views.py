from .models import Location, Article
from .serializers import LocationSerializer, LocationArticleSerializer

from django.shortcuts import get_object_or_404

from mezzanine.utils.views import render

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'locations': reverse('api-location-list', request=request),
    })


class LocationList(generics.ListAPIView):
    model = Location
    serializer_class = LocationSerializer


class LocationDetail(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationSerializer


class LocationArticle(generics.RetrieveAPIView):
    model = Location
    serializer_class = LocationArticleSerializer


def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    templates = [u"article/location_detail.html"]
    c = {"location": location}
    return render(request, templates, c)


def topic_detail(request, slug):
    blog_posts = Article.topics.published(for_user=request.user).select_related()
    return blog_detail(blog_posts, request, slug)


def article_detail(request, slug):
    blog_posts = Article.articles.published(for_user=request.user).select_related()
    return blog_detail(blog_posts, request, slug)


def blog_detail(blog_posts, request, slug, template="blog/blog_post_detail.html"):
    blog_post = get_object_or_404(blog_posts, slug=slug)
    context = {"blog_post": blog_post, "editable_obj": blog_post}
    templates = [u"blog/blog_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)
