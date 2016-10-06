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
