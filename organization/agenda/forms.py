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
from organization.magazine.models import Article
from organization.pages.models import CustomPage
from organization.agenda.models import Event, DynamicContentEvent,\
    EventPersonListBlockInline, DynamicMultimediaEvent
from organization.media.forms import DynamicMultimediaForm
from organization.network.models import PersonListBlock, Person


class DynamicContentEventForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=None,
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2(
            'dynamic-content-event'
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DynamicContentEventForm, self).__init__(*args, **kwargs)
        self.fields['content_object'].queryset = autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all(),
            Person.objects.all()
        )

    class Meta:
        model = DynamicContentEvent
        fields = ('content_object',)


class DynamicMultimediaEventForm(DynamicMultimediaForm):

    class Meta(DynamicMultimediaForm.Meta):
        model = DynamicMultimediaEvent


class EventPersonListForm(forms.ModelForm):

    person_list_block = forms.ModelChoiceField(
        queryset=None,
        widget=autocomplete.ModelSelect2(url='person-list-block-autocomplete')
    )

    def __init__(self, *args, **kwargs):
        super(EventPersonListForm, self).__init__(*args, **kwargs)
        self.fields['content_object'].queryset = PersonListBlock.objects.all()

    class Meta:
        model = EventPersonListBlockInline
        fields = ('person_list_block',)
