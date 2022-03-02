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
from organization.agenda.models import Event, DynamicContentEvent
from organization.media.models import Playlist
from organization.media.forms import DynamicMultimediaForm
from organization.network.models import Organization
from organization.projects.models import *
from extra_views import InlineFormSet


class DynamicContentProjectForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all(),
            Person.objects.all(),
            Organization.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-project'),
    )

    class Meta:
        model = DynamicContentProject
        fields = ('content_object',)


class ProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Project name"
        self.fields['title'].help_text =  "Acronym + full designation"
        self.fields['keywords'].help_text = "3 comma separated keywords"
        self.fields['date_from'].help_text = "Project start date (MM/DD/YYYY)"
        self.fields['date_to'].help_text = "Project end date (MM/DD/YYYY)"

    class Meta:
        model = Project
        fields = ('title', 'keywords', 'website', 'date_from', 'date_to')


class ProjectPublicDataInline(InlineFormSet):

    max_num = 1
    model = ProjectPublicData
    prefix = "Public data"
    can_delete = False
    fields = '__all__'


class ProjectPrivateDataInline(InlineFormSet):

    max_num = 1
    model = ProjectPrivateData
    prefix = "Private data"
    can_delete = False
    fields = '__all__'


class ProjectPrivateDataPublicFundingInline(InlineFormSet):

    max_num = 1
    model = ProjectPrivateData
    prefix = "Private data"
    can_delete = False
    fields = ("description", "funding_programme", "commitment_letter", "persons",)


class ProjectPrivateDataPrivateFundingInline(InlineFormSet):

    max_num = 1
    model = ProjectPrivateData
    prefix = "Private data"
    can_delete = False
    fields = ("description", "dimension", "commitment_letter", "investor_letter", "persons",)


class ProjectUserImageInline(InlineFormSet):

    extra = 3
    model = ProjectUserImage
    prefix = 'Private images'
    text = "To be published only for ICT-Projects selected by the consortium"
    can_delete = False
    fields = ['file', 'credits']


class ProjectLinkInline(InlineFormSet):

    extra = 3
    model = ProjectLink
    prefix = 'Public link'
    text = "To be published only for ICT-Projects selected by the consortium"
    can_delete = False
    fields = ['url', 'type']



class ProjectContactForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectContactForm, self).__init__(*args, **kwargs)
        self.fields['organization_name'].help_text = "The organization related to the contact"
        self.fields['position'].help_text = "The position of the contact in the organization"
        for field in self._meta.fields:
            self.fields[field].required = True

    class Meta:
        model = ProjectContact
        fields = ('first_name', 'last_name', 'email', 'organization_name',
                    'position', 'address', 'telephone', 'address', 'postal_code',
                    'city', 'country')


class ProjectContactInline(InlineFormSet):

    max_num = 1
    model = ProjectContact
    form_class = ProjectContactForm
    prefix = 'Private project contact'
    can_delete = False


class ProjectResidencyForm(ModelForm):

    class Meta:
        model = ProjectResidency
        fields = '__all__'


class Pivot_Project_ProjectCollection_Form(autocomplete.FutureModelForm):

    class Meta:
        model = Pivot_Project_ProjectCollection
        fields = ('__all__')
        widgets = {
            'projects': autocomplete.ModelSelect2Multiple(
                url='dynamic-collection-project',
                attrs={'data-html': True}
            )
        }


class DynamicMultimediaProjectForm(DynamicMultimediaForm):

    class Meta(DynamicMultimediaForm.Meta):
        model = DynamicMultimediaProject


class DynamicContentProjectPageForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all(),
            Person.objects.all(),
            Organization.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-project'),
    )

    class Meta:
        model = DynamicContentProjectPage
        fields = ('content_object',)


class TopicFilterForm(forms.Form):

    def get_topics():
        topics = ProjectTopic.objects.all()
        topics_list = []

        for topic in topics_list:
            if topic.projects.count():
                topics_list.append((topic.id, topic.name))
        return topics_list

    filter = forms.ChoiceField(choices=get_topics(), required=False)


class TypeFilterForm(forms.Form):

    filter = forms.ChoiceField(choices=PROJECT_TYPE_CHOICES, required=False)
