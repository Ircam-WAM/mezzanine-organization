from dal import autocomplete

import dal_queryset_sequence
import dal_select2_queryset_sequence

from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import CustomPage
from organization.pages.models import *
from organization.agenda.models import Event
from organization.media.models import Audio, Video

class DynamicContentHomeSliderForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-home-slider'),
    )

    class Meta:
        model = DynamicContentHomeSlider
        fields = ('content_object',)


class DynamicContentHomeBodyForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Brief.objects.all(),
            Event.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-home-body'),
    )

    class Meta:
        model = DynamicContentHomeBody
        fields = ('content_object',)


class DynamicContentHomeMediaForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Audio.objects.all(),
            Video.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-home-media'),
    )

    class Meta:
        model = DynamicContentHomeMedia
        fields = ('content_object',)



class DynamicContentPageForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-page'),
    )

    class Meta:
        model = DynamicContentPage
        fields = ('content_object',)
