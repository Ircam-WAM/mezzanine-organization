import os
from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from mezzanine.conf import settings
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

        job_offer = JobOffer.objects.get(slug=self.kwargs['slug'])
        email_application_notification(self.request, job_offer, form.cleaned_data)
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


def email_application_notification(request, job_offer, data):
    subject = "Candidature > " + job_offer.title
    to = [job_offer.email if job_offer.email else settings.DEFAULT_TO_EMAIL]
    from_email = settings.DEFAULT_FROM_EMAIL

    ctx = {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
    }

    message = get_template('core/email/application_notification.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.attach(data['curriculum_vitae'].name, data['curriculum_vitae'].read(), data['curriculum_vitae'].content_type)
    msg.attach(data['cover_letter'].name, data['cover_letter'].read(), data['cover_letter'].content_type)
    msg.content_subtype = 'html'
    msg.send()

    return HttpResponse('email_application_notification')
