# -*- coding: utf-8 -*-
from django.http import QueryDict
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
from mezzanine.template import Library
from mezzanine_agenda.models import Event
from mezzanine.conf import settings
from random import shuffle

from organization.festival.models import *
from organization.magazine.models import *
from organization.projects.models import *

register = Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.as_tag
def children_pages(page_id):
    childrens = Page.objects.filter(parent_id=page_id).order_by('_order')
    if childrens:
        return childrens
    return None

@register.as_tag
def featured_edito(*args):
    qs = Page.objects.filter(slug="edito")
    if qs:
        return qs[0].get_content_model()
    else:
        return None

@register.as_tag
def featured_events(*args):
    featured = Featured.objects.all()
    if featured:
        return featured[0].events.order_by('start')
    return None

@register.as_tag
def featured(*args):
    featured_list = []
    featured = Featured.objects.filter(id=settings.HOME_FEATURED_ID)
    if featured:
        featured = featured[0]
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
    featured = Featured.objects.filter(id=settings.BREAKING_NEWS_FEATURED_ID)
    if featured:
        featured = featured[0]
        news = featured.pages.all()
        if news:
            return news[0].richtextpage.content
        else:
            return ''
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

@register.filter
def no_parents(events):
    return events.filter(parent=None)

@register.filter
def get_mezzanine_menu_name(menu_id):
    return settings.PAGE_MENU_TEMPLATES[int(menu_id)-1][1]
    #return getattr(settings, 'PAGE_MENU_TEMPLATES', menu_id)

@register.filter
def get_type(objects, type):
    if objects:
        objs = objects.filter(type=type)
        if objs:
            return objs
    return None

@register.filter
def get_type_link(objects, name):
    objs = objects.filter(link_type__name=name)
    if objs:
        return objs
    return None

@register.filter
def in_category(objects, category):
    return objects.filter(category=type)

@register.filter
def sub_topics(topic):
    return ProjectTopic.objects.filter(parent=topic)

@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.filter
def app_label_short(obj):
    app_label = obj._meta.app_config.label
    if app_label.find("_") > 0:
        app_label_short = app_label.split("_")[1]
    elif app_label.find("-") > 0:
        app_label_short = app_label.split("-")[1]
    else :
        app_label_short = app_label
    return app_label_short

@register.as_tag
def activity_statuses(*args):
    return ActivityStatus.objects.filter(display=True)

@register.filter
def get_team_persons(status, team):
    persons = []
    for activity in status.activities.filter(teams__in=[team]):
        if not activity.person in persons:
            persons.append(activity.person)
    return persons
