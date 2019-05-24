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
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import CustomPage
from organization.agenda.models import Event, DynamicContentEvent, EventPersonListBlockInline, DynamicMultimediaEvent
from organization.media.models import Playlist, Media
from organization.media.forms import DynamicMultimediaForm
from organization.network.models import PersonListBlock, Person


class DynamicContentEventForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all(),
            Person.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-event'),
    )

    class Meta:
        model = DynamicContentEvent
        fields = ('content_object',)


class DynamicMultimediaEventForm(DynamicMultimediaForm):
    
    class Meta(DynamicMultimediaForm.Meta):
        model = DynamicMultimediaEvent
    

class EventPersonListForm(forms.ModelForm):
    
    person_list_block = forms.ModelChoiceField(
        queryset=PersonListBlock.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-list-block-autocomplete')
    )

    class Meta:
        model = EventPersonListBlockInline
        fields = ('person_list_block',)