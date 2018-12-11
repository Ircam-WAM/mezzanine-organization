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

from django.utils import timezone
from dal import autocomplete
import dal_queryset_sequence
import dal_select2_queryset_sequence
from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.projects.models import ProjectWorkPackage
from organization.network.models import *
from organization.pages.models import Page, CustomPage
from organization.network.utils import timesheet_master_notification_for_validation
from organization.network.models import *
from organization.pages.models import Page, CustomPage
from organization.media.forms import DynamicMultimediaForm
from extra_views import InlineFormSet


class PageCustomPersonListForm(forms.ModelForm):

    person_list_block = forms.ModelChoiceField(
        queryset=PersonListBlock.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-list-block-autocomplete')
    )

    class Meta:
        model = PageCustomPersonListBlockInline
        fields = ('person_list_block',)


class PersonListBlockInlineForm(forms.ModelForm):

    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-autocomplete')
    )

    class Meta:
        model = PersonListBlockInline
        fields = ('__all__')


class OrganizationLinkedListForm(forms.ModelForm):

    organization_linked = forms.ModelChoiceField(
        queryset=OrganizationLinked.objects.all(),
        widget=autocomplete.ModelSelect2(url='organization-linked-list-autocomplete')
    )

    class Meta:
        model = OrganizationLinkedBlockInline
        fields = ('organization_linked',)


class OrganizationLinkedForm(forms.ModelForm):

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=autocomplete.ModelSelect2(url='organization-linked-autocomplete')
    )

    class Meta:
        model = OrganizationLinkedInline
        fields = ('organization',)


class PersonActivityTimeSheetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonActivityTimeSheetForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs :
            self.fields['work_packages'].queryset = ProjectWorkPackage.objects.filter(project=kwargs['initial']['project'])
            self.fields['project'].choices = ((kwargs['initial']['project'].id, kwargs['initial']['project']),)
            self.fields['activity'].choices = ((kwargs['initial']['activity'].id, kwargs['initial']['activity']),)
        if self.fields['work_packages'].choices.__len__() == 0:
            self.fields['work_packages'].widget = forms.MultipleHiddenInput()
        else:
            self.fields['work_packages'].widget = forms.CheckboxSelectMultiple(choices=self.fields['work_packages'].choices)

    def save(self):
        self.instance.accounting = timezone.now()
        # send mail
        super(PersonActivityTimeSheetForm, self).save()
        timesheet_master_notification_for_validation(self.instance.activity.person,
                                                    self.instance.month,
                                                    self.instance.year,
                                                    self.instance._meta.app_config.label,
                                                    self.instance.__class__.__name__)

    class Meta:
        model = PersonActivityTimeSheet
        fields = ('__all__')
        exclude = ['accounting', 'validation', 'month', 'year']


class PersonActivityTimeSheetAdminForm(forms.ModelForm):

    class Meta:
        model = PersonActivityTimeSheet
        fields = ('__all__')
        widgets = {
            'activity': autocomplete.ModelSelect2(
                url='person-activity-autocomplete',
                attrs={'data-html': True}
            ),
            'work_packages': autocomplete.ModelSelect2Multiple(
                url='work-packages-autocomplete',
                attrs={'data-html': True}
            )
        }


class ProjectActivityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectActivityForm, self).__init__(*args, **kwargs)
        self.fields['work_packages'].queryset = ProjectWorkPackage.objects.filter(project=self.instance.project)
        self.fields['work_packages'].widget = forms.CheckboxSelectMultiple(choices=self.fields['work_packages'].choices)

    class Meta:
        model = ProjectActivity
        fields = ('__all__')
        exclude = ['accounting', 'validation']
        help_texts = {
            'work_packages': 'Set percentage between 0 and 100',
        }


class OrganizationContactInline(InlineFormSet):

    max_num = 1
    model = OrganizationContact
    prefix = 'Contact'
    can_delete = False
    fields = ['person_title', 'first_name', 'last_name', 'email', 'telephone', 'role']


class OrganizationUserImageInline(InlineFormSet):

    max_num = 4
    model = OrganizationUserImage
    prefix = 'Images'
    can_delete = False
    fields = ['file', 'credits']


class OrganizationForm(ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'description', 'url', 'address',
                  'address', 'postal_code', 'city', 'country',]


class ProducerDataInline(InlineFormSet):

    max_num = 1
    model = ProducerData
    prefix = "Descriptions"
    can_delete = False
    fields = ['producer_description', 'experience_description']

    def get_factory_kwargs(self):
        kwargs = super().get_factory_kwargs()
        kwargs.update({"min_num": 1})
        return kwargs


class ProducerForm(ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'url', 'email', 'telephone', 'address', 'postal_code', 'city', 'country',]

    def __init__(self, *args, **kwargs):
        super(ProducerForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True


class DynamicMultimediaOrganizationForm(DynamicMultimediaForm):
    
    class Meta(DynamicMultimediaForm.Meta):
        model = DynamicMultimediaOrganization


class DynamicMultimediaPersonForm(DynamicMultimediaForm):
    
    class Meta(DynamicMultimediaForm.Meta):
        model = DynamicMultimediaPerson