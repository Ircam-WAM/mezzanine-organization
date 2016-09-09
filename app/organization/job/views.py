import os
from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from organization.job.models import JobOffer, JobResponse
from organization.job.forms import JobResponseForm

extention = ['.pdf', '.PDF', '.doc', '.docx']

class JobOfferDetailView(CreateView):

    model = JobResponse
    template_name='job/job_offer_detail.html'
    context_object_name = 'job_offer'
    form_class = JobResponseForm

    def get_context_data(self, **kwargs):
        context = super(JobOfferDetailView, self).get_context_data(**kwargs)
        job_offer = JobOffer.objects.get(slug=self.kwargs['slug'])
        if job_offer :
            context['job_offer'] = job_offer
        return context

    def get_initial(self):
        initial = super(JobOfferDetailView, self).get_initial()
        job_offer = JobOffer.objects.get(slug=self.kwargs['slug'])
        if job_offer :
            initial['job_offer'] = job_offer
        return initial

    def get_success_url(self):
        return reverse_lazy('organization-job-offer-detail', kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        # check extension uploaded files
        name_cv, ext_cv = os.path.splitext(form.cleaned_data['curriculum_vitae'].name)
        name_cl, ext_cl = os.path.splitext(form.cleaned_data['cover_letter'].name)
        if ext_cv not in extention or ext_cl not in extention :
            messages.info(self.request, _("Only .pdf, .doc, .docx files allowed."))
            return super(JobOfferDetailView, self).form_invalid(form)
        messages.info(self.request, _("You have successfully submitted your application."))
        return super(JobOfferDetailView, self).form_valid(form)


class JobOfferListView(ListView):

    model = JobOffer
    template_name='job/job_offer_list.html'
    context_object_name = 'job_offer'

    def get_queryset(self, **kwargs):
        return self.model.objects.published()

    def get_context_data(self, **kwargs):
        context = super(JobOfferListView, self).get_context_data(**kwargs)
        return context
