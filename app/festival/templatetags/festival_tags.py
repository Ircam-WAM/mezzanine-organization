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
    return Featured.objects.all()[0].events.order_by('start')

@register.as_tag
def featured(*args):
    return Featured.objects.get(id=settings.HOME_FEATURED_ID)


@register.as_tag
def featured_breaking_news_content(*args):
    news = Featured.objects.get(id=settings.BREAKING_NEWS_FEATURED_ID).pages.all()
    if news:
        return news[0].richtextpage.content
    return ''
