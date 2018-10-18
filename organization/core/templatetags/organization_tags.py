# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
import datetime
import calendar
import ast
import re
from re import match
from django.http import QueryDict
from mezzanine.pages.models import Page
from mezzanine.blog.models import BlogPost
from mezzanine.template import Library
from mezzanine_agenda.models import Event
from mezzanine.conf import settings
from random import shuffle
from django.utils.translation import ugettext_lazy as _
from organization.agenda.models import EventPeriod
from organization.magazine.models import *
from organization.projects.models import *
from django.utils.formats import get_format
from django.utils.dateformat import DateFormat
from organization.core.models import *
from itertools import chain
from django.db.models import Q
from organization.pages.models import ExtendedCustomPageDynamicContent as ECPDC
from django.core import serializers
from django.utils.functional import allow_lazy
from django.utils import six

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
            if not post in post_list:
                post_list.append(post)
    return post_list

@register.filter
def no_parents(events):
    return events.filter(parent=None)

@register.filter
def get_mezzanine_menu_name(menu_id):
    if menu_id:
        return settings.PAGE_MENU_TEMPLATES[int(menu_id)-1][1]
    return 'None'

@register.as_tag
def get_pages_in_menu(menu_id):
    return Page.objects.filter(in_menus=str(menu_id)).order_by("_order")

@register.filter
def get_type(objects, type):
    if objects:
        objs = objects.filter(type=type)
        if objs:
            return objs
    return None

@register.filter
def get_type_link(objects, slug):
    objs = objects.filter(link_type__slug=slug)
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
    return ActivityStatus.objects.filter(display=True).exclude(parent__isnull=False)

@register.filter
def get_team_persons(team, status):
    persons = []
    statuses = status.children.all()
    if not statuses:
        statuses = [status,]
    for status in statuses:
        activities = status.activities.filter(teams__in=[team], date_to__gte=datetime.date.today())
        for activity in activities:
            if not activity.person in persons:
                persons.append(activity.person)
    return persons

@register.filter
def slice_ng(qs, indexes):
    list = []
    for obj in qs:
        list.append(obj)
    index_split = indexes.split(':')
    index_1 = int(index_split[0])
    index_2 = 0
    if len(index_split) > 1:
        index_2 = int(index_split[1])
    if index_1 >= 0 and index_2:
        return list[index_1:index_2]
    else:
        return [list[index_1]]

@register.filter
def date_year_higher_than(date, years):
    diff = date - datetime.date.today()
    print(diff.days)
    return diff.days > years*365

@register.simple_tag
def current_year():
    return datetime.datetime.now().strftime("%Y")

@register.filter
def is_not_host(organizations):
    return organizations.exclude(is_host=True)

@register.filter
def unspam(email):
    return email.replace('@', ' (at) ')

@register.filter
def get_attr(obj, attr):
    return getattr(obj, attr)

@register.filter
def month_name(month_number):
    if isinstance(month_number, str):
        month_number = int(month_number)
    return _(calendar.month_name[month_number])

@register.filter
def format_wp(work_packages):
    work_packages = [str(wk.number) for wk in work_packages]
    return ",".join(work_packages)

@register.filter
def format_percent(percent):
    return str(percent * 100) + ' %'

@register.filter
def get_media_type(media):
    mime_type = media.transcoded.first().mime_type
    media_type = ""
    if match('video', mime_type):
        media_type = "Video"
    elif match('audio', mime_type):
        media_type = "Audio"
    return media_type

@register.filter
def filter_content(dynamic_contents):
    dict = {}
    dict["event"] = []
    dict["other"] = []
    for dc in dynamic_contents:
        if dc.content_object:
            if dc.content_object._meta.model_name== "event":
                dict["event"].append(dc)
            else :
                dict["other"].append(dc)
    return dict

@register.filter
def get_vars(object):
    return vars(object)

@register.filter
def has_alinea(page):
    if hasattr(page._custompage_cache, 'menu_alinea'):
        return page._custompage_cache.menu_alinea

@register.filter
def get_value(dict, value):
    if dict.__class__.__name__ == "str":
        dict = ast.literal_eval(dict)
    return dict[value]

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter
def get_separator_with(date_start, date_end):
    separator = ""
    # several days between two dates
    if date_end:
        diff = date_end - date_start
        diff = diff.days * 24 + diff.seconds/3600
        if diff > 24 :
            separator = _("through")
        # less than 24 hours between two dates
        else :
            separator = _("and")
    return separator


@register.filter
def format_date_fct_of(date_start, date_end):
    date_start = DateFormat(date_start)
    date_start = date_start.format(get_format('DATE_EVENT_FORMAT'))
    if date_end:
        date_end = DateFormat(date_end)
        if date_start.format(get_format('SHORT_DATE_FORMAT')) == date_end.format(get_format('SHORT_DATE_FORMAT')):
            date_start = date_start.format(get_format('DATE_EVENT_FORMAT'))
        elif date_start.format(get_format('YEAR_MONTH_FORMAT')) == date_end.format(get_format('YEAR_MONTH_FORMAT')):
            date_start = date_start.format(get_format('WEEK_DAY_FORMAT'))
    return date_start


@register.filter
def period_is_more_than_hours(date_obj, hours):
    is_more = False
    if isinstance(date_obj, EventPeriod):
        is_more = is_more_then_hours(date_obj.date_from, date_obj.date_to, hours)
    if isinstance(date_obj, Event):
        is_more = is_more_then_hours(date_obj.start, date_obj.end, hours)
    return is_more

def is_more_then_hours(date_begin, date_end, hours):
    if not date_end:
        is_more = False
    else :
        is_more = (date_end - date_begin).seconds > hours*3600
    return is_more


@register.filter
def get_article_by_department(department):
    return Article.objects.published().filter(department=department).order_by('-publish_date')[:3]


@register.filter
def get_first_brief(object_list):
    brief_obj = object_list.filter(content_type__model="brief").first()
    content_obj = None
    if brief_obj:
        content_obj = brief_obj.content_object
    return content_obj

@register.filter
def order_links(links):
    links_list = list(links)
    ordered_links = []
    while links_list:
        minor = links_list[0]
        for link in links_list:
            try:
                if (link.link_type.ordering < minor.link_type.ordering):
                    minor = link
            except TypeError:
                pass
        ordered_links.append(minor)
        links_list.remove(minor)
    return ordered_links

@register.filter
def extended_custompage_extra_content(extra_content):
    context = {}
    if extra_content.choice == ECPDC.LIST_NEWS:
        news = Article.objects.all()
        news = news.filter(status=2)
        medias = Media.objects.published()
        news = sorted(
            chain(news, medias),
            key=lambda instance: instance.created,
            reverse=True)
        context["news"] = news
    elif extra_content.choice == ECPDC.LIST_EVENTS:
        events = Event.objects.published()
        context["events"] = events.filter(Q(start__gt=datetime.datetime.now()) | Q(end__gt=datetime.datetime.now()))
        context["past_events"] = events.filter(end__lt=datetime.datetime.now()).order_by("start")
    elif extra_content.choice == ECPDC.LIST_JURY:
        jury = PersonListBlock.objects.filter(title__in=["Jury", "jury"])
        if jury:
            jury_list = Person.objects.filter(person_list_block_inlines__person_list_block=jury).order_by("last_name")
        else:
            jury_list = Person.objects.none()
        context["jury"] = jury_list
    return context

@register.filter
def hal_1(hal_tutelage, hal_researche_structure):
    return settings.HAL_URL_PART_1 % (hal_researche_structure.replace(' ', '+'), hal_tutelage.replace(' ', '+'))

@register.filter
def hal_2(url_part, http_host):
    return url_part + settings.HAL_URL_PART_2 % http_host

@register.filter
def tag_is_in_menu(page, tag):
    is_in_menu = False
    if tag and page :
        if page.slug.lower().find(tag.slug.lower()) != -1:
            is_in_menu = True
    return is_in_menu

@register.filter(is_safe=True)
def removetags(value, tags):
    """Removes a space separated list of [X]HTML tags from the output."""
    return remove_tags(value, tags)

def remove_tags(html, tags):
    """Returns the given HTML with given tags removed."""
    warnings.warn(
        "django.utils.html.remove_tags() and the removetags template filter "
        "are deprecated. Consider using the bleach library instead.",
        RemovedInDjango110Warning, stacklevel=3
    )
    tags = [re.escape(tag) for tag in tags.split()]
    tags_re = '(%s)' % '|'.join(tags)
    starttag_re = re.compile(r'<%s(/?>|(\s+[^>]*>))' % tags_re, re.U)
    endtag_re = re.compile('</%s>' % tags_re)
    html = starttag_re.sub('', html)
    html = endtag_re.sub('', html)
    return html
remove_tags = allow_lazy(remove_tags, six.text_type)

@register.filter
def serialize(value, serializer="json"):
    return mark_safe(serializers.serialize(serializer, value, use_natural_foreign_keys=True, use_natural_primary_keys=True, indent=2))

@register.filter
def props_filter(iterable, conditions):
    """
    Filter an iterable following `conditions` (joined by AND)

    Conditions example : `{'prop': 'value'}`
    -> Will filter items having item.prop='value'
    """

    # SMELL: should not be a security issue as long as `conditions` does not include variables
    conditions = eval(str(conditions))
    if not isinstance(conditions, dict):
        return iterable

    def satisfies_conditions(item):
        included = True
        for c, v in conditions.items():
            if c not in item or item[c] != v:
                included = False
        return included

    ret = [item for item in iterable if satisfies_conditions(item)]

    return ret

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)