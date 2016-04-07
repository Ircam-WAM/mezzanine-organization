# -*- coding: utf-8 -*-
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
from mezzanine.template import Library
from mezzanine_agenda.models import Event
from festival.models import *
from mezzanine.conf import settings

register = Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.as_tag
def featured_edito(*args):
    qs = Page.objects.filter(slug="edito")
    if qs:
        return qs[0].get_content_model()
    else:
        return None

@register.as_tag
def featured_events(*args):
    models = [Event,]
    featured = []
    for model in models:
        objs = model.objects.filter(featured=True)
        for obj in objs:
            if hasattr(obj, 'featured_image_header'):
                featured.append(obj)
    return featured

@register.as_tag
def featured_artist(*args):
    return Artist.objects.filter(featured=True).order_by('?').first()

@register.as_tag
def featured_video(*args):
    return Video.objects.filter(featured=True).order_by('?').first()

@register.as_tag
def featured_playlist(*args):
    return Playlist.objects.filter(event=None).order_by('?').first()

@register.as_tag
def featured_pages(*args):
    return Page.objects.filter(featured=True)

@register.as_tag
def featured_posts(*args):
    return BlogPost.objects.all()[0]
