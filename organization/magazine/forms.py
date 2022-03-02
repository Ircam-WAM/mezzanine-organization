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

from dal import autocomplete
import dal_queryset_sequence
import dal_select2_queryset_sequence
from django import forms
from django.forms.utils import ErrorList
from organization.magazine.models import *
from organization.pages.models import CustomPage
from organization.network.models import PersonListBlock, Person
from organization.network.views import TeamOwnableMixin
from mezzanine_agenda.models import Event
from organization.media.forms import DynamicMultimediaForm
from mezzanine.blog.models import BlogCategory
from mezzanine_agenda.models import EventCategory


class BriefForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            Event.objects.all(),
            CustomPage.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('object-autocomplete'),
    )

    class Meta:
        model = Brief
        fields = ('__all__')


class ArticlePersonListForm(forms.ModelForm):

    person_list_block = forms.ModelChoiceField(
        queryset=PersonListBlock.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-list-block-autocomplete')
    )

    class Meta:
        model = ArticlePersonListBlockInline
        fields = ('person_list_block',)


class DynamicContentArticleForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            Event.objects.all(),
            CustomPage.objects.all(),
            Person.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-article'),
    )

    class Meta:
        model = DynamicContentArticle
        fields = ('content_object',)


class DynamicMultimediaArticleForm(DynamicMultimediaForm):
    
    class Meta(DynamicMultimediaForm.Meta):
        model = DynamicMultimediaArticle


class CategoryFilterForm(forms.Form, TeamOwnableMixin):

    categories = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):

        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        self.process_choices()

    def process_choices(self, team=None):
        CATEGORIES = []
        articles = Article.objects.published()
        if team:
            articles = self.filter_by_team(articles, team)

        used_art_cat = articles.values_list('categories__id', flat=True) \
                        .order_by('categories__id') \
                        .distinct('categories__id') \

        blog_categories = BlogCategory.objects.filter(id__in=used_art_cat)
        for category in blog_categories:
            CATEGORIES.append((category.id, category.title))
        
        # try / except > for passing migration mezzanine_agenda-0031
        from django.db import DatabaseError
        try:
            events = Event.objects.published()
            if team :
                events = self.filter_by_team(events, team)
            used_evt_cat = events.values_list('category__id', flat=True) \
                                .order_by('category__id') \
                                .distinct('category__id')
            if team :
                used_evt_cat = self.filter_by_team(used_evt_cat, team)
            event_categories = EventCategory.objects.filter(id__in=used_evt_cat)
            for category in event_categories:
                CATEGORIES.append((category.id, category.name))
        except DatabaseError:
            pass

        self.fields['categories'].choices = CATEGORIES


class DynamicContentMagazineContentForm(autocomplete.FutureModelForm):
    
    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            Playlist.objects.all(),
            Media.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-magazine'),
    )

    class Meta:
        model = DynamicContentMagazineContent
        fields = ('content_object',)
