from dal import autocomplete

from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from organization.job.models import JobResponse


class JobResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(JobResponseForm, self).__init__(*args, **kwargs)
        self.fields['job_offer'].widget = forms.HiddenInput()

    class Meta:
        model = JobResponse
        fields = ['first_name', 'last_name', 'email', 'curriculum_vitae', 'cover_letter', 'job_offer']
