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
from organization.job.models import *
from organization.magazine.models import Article
from organization.pages.models import CustomPage
from mezzanine_agenda.models import Event


class JobResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(JobResponseForm, self).__init__(*args, **kwargs)
        self.fields['job_offer'].widget = forms.HiddenInput()

    class Meta:
        model = JobResponse
        fields = ['first_name', 'last_name', 'email', 'message', 'curriculum_vitae', 'cover_letter', 'job_offer']


class CandidacyForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            Event.objects.all(),
            CustomPage.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('candidacy-autocomplete'),
    )

    class Meta:
        model = Candidacy
        fields = ('__all__')
