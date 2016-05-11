# -*- coding: utf-8 -*-
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
from mezzanine.template import Library
from mezzanine_agenda.models import Event
from festival.models import *
from mezzanine.conf import settings
from random import shuffle

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
    featured = Featured.objects.get(id=settings.HOME_FEATURED_ID)
    featured_list = []
    for post in featured.blogposts.all():
        featured_list.append(post)
    for video in featured.videos.all():
        featured_list.append(video)
    for artist in featured.artists.all():
        featured_list.append(artist)
    for playlist in featured.playlists.all():
        featured_list.append(playlist)
    shuffle(featured_list)
    return featured_list

@register.as_tag
def featured_breaking_news_content(*args):
    news = Featured.objects.get(id=settings.BREAKING_NEWS_FEATURED_ID).pages.all()
    if news:
        return news[0].richtextpage.content
    return ''

@register.filter
def get_class(obj):
    return obj.__class__.__name__

@register.filter
def unique_posts(events):
    post_list = []
    for event in events:
        for post in event.blog_posts.all():
            print(post)
            if not post in post_list:
                post_list.append(post)
    return post_list
