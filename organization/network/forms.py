from dal import autocomplete
import dal_queryset_sequence
import dal_select2_queryset_sequence
from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.network.models import Person
from organization.network.models import PersonListBlock, DynamicPersonList #DynamicContentPersonList,
from organization.pages.models import DynamicPersonListBlockPage


class DynamicPersonListForm(autocomplete.FutureModelForm):
    """
    List of Person
    """
    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Person.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-person-list'),
    )

    class Meta:
        model = DynamicPersonList
        fields = ('content_object',)


class DynamicContentPersonListBlockForm(autocomplete.FutureModelForm):
    """
    List of PersonListBlock
    """
    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            PersonListBlock.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-person-list-block'),
    )

    class Meta:
        model = DynamicPersonListBlockPage
        fields = ('content_object',)
