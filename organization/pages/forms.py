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

import datetime
from dal import autocomplete

import dal_queryset_sequence
import dal_select2_queryset_sequence
from cartridge.shop.models import Product
from django import forms
from mezzanine.conf import settings
from organization.magazine.models import Article, Brief
from organization.pages.models import CustomPage
from organization.media.models import Playlist, Media
from organization.network.models import Person
from organization.projects.models import Project
from organization.pages.models import DynamicContentHomeSlider,\
    DynamicContentHomeBody, DynamicContentHomeMedia, ExtendedCustomPage,\
    DynamicContentPage, DynamicMultimediaPage
from mezzanine_agenda.models import Event
from organization.media.forms import DynamicMultimediaForm
from organization.projects.models import ProjectPage


class DynamicContentHomeSliderForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=None,
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2(
            'dynamic-content-home-slider'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DynamicContentHomeSliderForm, self).__init__(*args, **kwargs)
        self.fields['content_object'].queryset = autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all(),
            Person.objects.all(),
            Media.objects.all()
        )

    class Meta:
        model = DynamicContentHomeSlider
        fields = ('content_object',)


class DynamicContentHomeBodyForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=None,
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2(
            'dynamic-content-home-body'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DynamicContentHomeBodyForm, self).__init__(*args, **kwargs)
        self.fields['content_object'].queryset = autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all(),
            Brief.objects.all(),
            Media.objects.all(),
            Person.objects.all(),
            Project.objects.all(),
            Playlist.objects.all()
        )

    class Meta:
        model = DynamicContentHomeBody
        fields = ('content_object',)


class DynamicContentHomeMediaForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=None,
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2(
            'dynamic-content-home-media'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DynamicContentHomeMediaForm, self).__init__(*args, **kwargs)
        self.fields['content_object'].queryset = autocomplete.QuerySetSequence(
            Playlist.objects.all(),
        )

    class Meta:
        model = DynamicContentHomeMedia
        fields = ('content_object',)


class DynamicContentPageForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=None,
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2(
            'dynamic-content-page'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DynamicContentPageForm, self).__init__(*args, **kwargs)
        self.fields['content_object'].queryset = autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all(),
            ExtendedCustomPage.objects.all(),
            ProjectPage.objects.all(),
            Product.objects.all()
        )

    class Meta:
        model = DynamicContentPage
        fields = ('content_object',)


class DynamicMultimediaPageForm(DynamicMultimediaForm):

    class Meta(DynamicMultimediaForm.Meta):
        model = DynamicMultimediaPage


class YearForm(forms.Form):

    curr_year = datetime.datetime.today().year
    year_list = reversed(range(settings.HAL_YEAR_BEGIN, curr_year + 1))
    YEARS = []
    for year in year_list:
        YEARS.append((str(year), str(year)))

    year = forms.ChoiceField(choices=YEARS)
