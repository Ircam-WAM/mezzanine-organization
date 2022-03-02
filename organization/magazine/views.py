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
from collections import OrderedDict
from re import match
from urllib.parse import urlparse
from django.utils import timezone
from django.urls import reverse_lazy
#from django.views.generic import *
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import *
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine_agenda.models import Event
from mezzanine.utils.views import paginate
from mezzanine.conf import settings
from mezzanine.generic.models import AssignedKeyword
from organization.magazine.models import *
from organization.network.models import DepartmentPage, Person
from organization.network.views import TeamOwnableMixin
from organization.pages.models import CustomPage, DynamicContentPage
from organization.core.views import SlugMixin, autocomplete_result_formatting, \
                                    DynamicContentMixin, FilteredListView, \
                                    RedirectContentView, DynamicReverseMixin
from organization.core.utils import split_events_from_other_related_content
from django.template.defaultfilters import slugify
from itertools import chain
from django.views.generic.edit import FormView
from .forms import CategoryFilterForm


class ArticleDetailView(RedirectContentView, SlugMixin, DetailView,
                        DynamicContentMixin, DynamicReverseMixin):

    model = Article
    template_name='magazine/article/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        articles = self.model.objects.published(for_user=self.request.user).select_related()
        return get_object_or_404(articles, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)

        if self.object.department:
            first_page = self.object.department.pages.first()
            if first_page:
                context['department_weaving_css_class'] = first_page.weaving_css_class
            context['department_name'] = self.object.department.name
        return context


class BriefDetailView(SlugMixin, DetailView):

    model = Brief
    template_name='magazine/inc_brief.html'
    context_object_name = 'brief'

    def get_context_data(self, **kwargs):
        context = super(BriefDetailView, self).get_context_data(**kwargs)
        return context


class BriefListView(SlugMixin, ListView):

    model = Brief
    template_name='magazine/brief/brief_list.html'
    context_object_name = 'brief'

    def get_context_data(self, **kwargs):
        context = super(BriefListView, self).get_context_data(**kwargs)
        return context


class TopicDetailView(SlugMixin, DetailView):

    model = Topic
    template_name='magazine/topic/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        # paginate "manually" articles because we are not in a ListView
        articles = paginate(self.object.articles.published(), self.request.GET.get("page", 1),
                          settings.ARTICLE_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
        context['articles'] = articles
        return context


class ObjectAutocomplete(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events )

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class DynamicContentArticleView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        events = Event.objects.all()
        pages = CustomPage.objects.all()
        persons = Person.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            pages = pages.filter(title__icontains=self.q)
            persons = persons.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, events, pages, persons)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class ArticleListView(ListView):

    model = Article
    template_name='magazine/article/article_list.html'
    context_object_name = 'objects'
    keywords = None

    def get_queryset(self):
        self.qs = self.model.objects.published(for_user=self.request.user).order_by('-created')
        if getattr(settings, 'ALLOW_PLAYLISTS_IN_ARTICLE', True):
            playlists = Playlist.objects.published().order_by('-created').distinct()

            if 'type' in self.kwargs:
                if self.kwargs['type'] == "article":
                    playlists = []

                if self.kwargs['type'] == "video" or self.kwargs['type'] == "audio":
                    playlists = playlists.filter(type=self.kwargs['type'])
                    self.qs = []

            self.qs = sorted(
                chain( self.qs, playlists),
                key=lambda instance: instance.created,
                reverse=True)

        if 'keyword' in self.kwargs:
            keywords = AssignedKeyword.objects.filter(keyword__slug=self.kwargs['keyword'])
            self.qs = self.qs.filter(keywords__in=keywords)

        return self.qs

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)

        if hasattr(settings, 'ARTICLE_KEYWORDS'):
            context['keywords'] = settings.ARTICLE_KEYWORDS

        # keywords
        assigned_keyword = AssignedKeyword()
        self.keywords = assigned_keyword.get_keywords_of_content_type(self.model._meta.app_label,
                                                                    self.model.__name__.lower())
        if self.keywords:
            context['keywords'] = self.keywords

        # pagination
        context['objects'] = paginate(self.qs, self.request.GET.get("page", 1),
                              settings.ARTICLE_PER_PAGE,
                              settings.MAX_PAGING_LINKS)

        # keyword by AssignKeyword
        if 'keyword' in self.kwargs:
            context['current_keyword_slug'] = self.kwargs['keyword']

        # keyword by MediaType: video, audio.....
        if 'type' in self.kwargs:
            context['current_keyword'] = self.kwargs['type'];

        return context


class ArticleListRedirect(RedirectView):

    permanent = True
    url = reverse_lazy('magazine-article-list')


class ArticleEventView(SlugMixin, ListView, FilteredListView):

    model = Article
    template_name='magazine/article/article_event_list.html'
    form_class = CategoryFilterForm
    keywords = OrderedDict()
    item_to_filter = "categories"
    property_query_filter = "categories__id"

    def get_queryset(self):
        self.qs = super(ArticleEventView, self).get_queryset()

        # get only published Articles and ordered by publish date
        self.qs = self.qs.filter(status=2).order_by('-publish_date')

        # get published Events
        events = Event.objects.published().order_by('-start').distinct()

        v_filter = None

        # Filter if GET
        if self.request.GET:
            if self.item_to_filter in self.request.GET.keys():
                form = self.get_form()
                v_filter = self._get_choice_id(self.request.GET[self.item_to_filter], form.fields[self.item_to_filter]._choices)

        # Filter if POST
        if self.filter_value:
            v_filter = self.filter_value

        # Apply filter
        if v_filter:
            kwargs = {
                '{0}'.format(self.property_query_filter): v_filter,
            }
            self.qs = self.qs.filter(**kwargs)
            events = events.filter(category__id=v_filter)

        self.qs = sorted(
            chain(self.qs, events),
            key=lambda instance:instance.publish_date,
            reverse=True)

        return self.qs

    def get_context_data(self, **kwargs):
        context = super(ArticleEventView, self).get_context_data(**kwargs)
        context['objects'] = paginate(self.qs, self.request.GET.get("page", 1),
                              settings.MEDIA_PER_PAGE,
                              settings.MAX_PAGING_LINKS)
        context['title'] = _('Laboratory News')
        return context


class ArticleEventTeamView(ArticleEventView, TeamOwnableMixin):

    def get_queryset(self):
        self.qs = super(ArticleEventTeamView, self).get_queryset()
        if 'slug' in self.kwargs:
            self.qs = self.filter_by_team(self.qs, self.kwargs['slug'])
        return self.qs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'slug' in self.kwargs:
            form.process_choices(self.kwargs['slug'])
        return super(ArticleEventTeamView, self).post(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleEventTeamView, self).get_context_data(**kwargs)
        context['form'].process_choices(self.kwargs['slug'])
        context['title'] = _('Team News')
        return context


class DynamicContentMagazineContentView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        playlists = Playlist.objects.all()
        medias = Media.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            playlists = playlists.filter(title__icontains=self.q)
            medias = medias.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, medias, playlists)
        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class MagazineDetailView(DetailView):

    model = Magazine
    template_name='magazine/magazine/magazine_detail.html'
    context_object_name = 'magazine'

    def get_object(self):
        try:
            obj = Magazine.objects.published().latest('publish_date')
        except Magazine.DoesNotExist:
            raise Http404("Magazine does not exist")
        return obj
