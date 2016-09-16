from dal import autocomplete
import dal_queryset_sequence
import dal_select2_queryset_sequence
from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.network.models import Person, PersonListBlock, DynamicPersonList, PersonAutocomplete #DynamicContentPersonList,
from organization.pages.models import DynamicPersonListBlockPage, Page


class PagePersonListForm(forms.ModelForm):

    person_list_block = forms.ModelChoiceField(
        queryset=PersonListBlock.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-list-block-autocomplete')
    )

    class Meta:
        model = Page
        fields = ('person_list_block',)


class PersonAutocompleteForm(forms.ModelForm):

    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-autocomplete')
    )

    class Meta:
        model = PersonAutocomplete
        fields = ('__all__')
