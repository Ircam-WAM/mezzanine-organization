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

import os
import mimetypes
import humanize
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
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
from django.shortcuts import get_object_or_404
from mezzanine.conf import settings
from organization.pages.models import CustomPage
from organization.magazine.models import Article
from organization.job.models import *
from organization.job.forms import JobResponseForm

mime_types = ['pdf', 'msword', 'vnd.oasis.opendocument.text', 'vnd.openxmlformats-officedocument.wordprocessingml.document']

class JobOfferDetailView(CreateView):

    model = JobResponse
    template_name='job/job_offer_detail.html'
    context_object_name = 'job_offer'
    form_class = JobResponseForm

    def get_context_data(self, **kwargs):
        context = super(JobOfferDetailView, self).get_context_data(**kwargs)
        context['job_offer'] = self.job_offer
        return context

    def get_initial(self):
        initial = super(JobOfferDetailView, self).get_initial()
        self.job_offer = get_object_or_404(JobOffer, slug=self.kwargs['slug'])
        initial['job_offer'] = self.job_offer
        return initial

    def get_success_url(self):
        return reverse_lazy('organization-job-offer-detail', kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        # check mimetype uploaded files
        mime_type_cv = form.cleaned_data['curriculum_vitae'].content_type.split('/')[1]
        mime_type_cl = form.cleaned_data['cover_letter'].content_type.split('/')[1]
        if mime_type_cv not in mime_types or mime_type_cl not in mime_types :
            messages.info(self.request, _("Only .pdf, .odt, .doc, .docx files allowed."))
            return super(JobOfferDetailView, self).form_invalid(form)
        # check max upload file for anonymous user
        if form.cleaned_data['curriculum_vitae'].size > settings.MAX_UPLOAD_SIZE_FRONT or form.cleaned_data['cover_letter'].size > settings.MAX_UPLOAD_SIZE_FRONT :
            messages.info(self.request, _("Uploaded files cannot exceed "+humanize.naturalsize(settings.MAX_UPLOAD_SIZE_FRONT)+"."))
            return super(JobOfferDetailView, self).form_invalid(form)
        email_application_notification(self.request, self.job_offer, form.cleaned_data)
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
        'message': data['message']
    }

    message = get_template('email/application_notification.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.attach(data['curriculum_vitae'].name, data['curriculum_vitae'].read(), data['curriculum_vitae'].content_type)
    msg.attach(data['cover_letter'].name, data['cover_letter'].read(), data['cover_letter'].content_type)
    msg.content_subtype = 'html'
    msg.send()

    return HttpResponse('email_application_notification')


class CandidacyListView(ListView):

    model = Candidacy
    template_name='job/candidacy_list.html'
    context_object_name = 'candidacy'

    def get_queryset(self, **kwargs):
        return self.model.objects.published()

    def get_context_data(self, **kwargs):
        context = super(CandidacyListView, self).get_context_data(**kwargs)
        return context


class CandidacyAutocomplete(Select2QuerySetSequenceView):
    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events )

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
