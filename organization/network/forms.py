from dal import autocomplete
import dal_queryset_sequence
import dal_select2_queryset_sequence
from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.network.models import (Person,
                                PersonListBlock,
                                PersonListBlockInline,
                                PageCustomPersonListBlockInline,
                                OrganizationLinked,
                                OrganizationLinkedInline,
                                OrganizationLinkedBlockInline,
                                Organization)
from organization.pages.models import Page, CustomPage


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
