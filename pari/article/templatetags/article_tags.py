from mezzanine import template

register = template.Library()


@register.inclusion_tag("article/includes/capsule_video.html")
def capsule_video_for(article, width, height):
    return {'article': article,
            'width': width,
            'height': height,
            }


@register.inclusion_tag("article/includes/featured_content.html")
def featured_content_for(article):
    return {'article': article}


@register.inclusion_tag("article/includes/article_list.html")
def article_list(articles, title, types, filter):
    return {'articles': articles, 'title': title, 'types': types, 'filter': filter}
