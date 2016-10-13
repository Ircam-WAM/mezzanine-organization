from dal import autocomplete

import dal_queryset_sequence
import dal_select2_queryset_sequence

from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.media.models import *


class PlaylistMediaForm(forms.ModelForm):

    media = forms.ModelChoiceField(
        queryset=Media.objects.all(),
        widget=autocomplete.ModelSelect2(url='media-autocomplete')
    )

    class Meta:
        model = PlaylistMedia
        fields = ('__all__')
