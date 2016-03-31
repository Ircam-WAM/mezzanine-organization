# -*- coding: utf-8 -*-
from mezzanine.pages.models import Page
from mezzanine.template import Library
from mezzanine_agenda.models import Event
from festival.models import Artist

register = Library()

@register.as_tag
def festival_edito(*args):
    qs = Page.objects.filter(slug="edito")
    if qs:
        return qs[0].get_content_model()
    else:
        return None

@register.as_tag
def festival_event_featured(*args):
    models = [Event,]
    featured = []
    for model in models:
        objs = model.objects.filter(featured=True)
        for obj in objs:
            if hasattr(obj, 'featured_image_header'):
                featured.append(obj)
    return featured

@register.filter
def subtract(value, arg):
    return value - arg
