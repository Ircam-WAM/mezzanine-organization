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

from itertools import chain
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.utils.translation import ugettext_lazy as _
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine_agenda.models import Event
from mezzanine.conf import settings
from organization.projects.models import *
from organization.projects.forms import *
from organization.network.forms import *
from organization.network.models import Organization
from organization.core.views import *
from organization.magazine.views import Article
from organization.pages.models import CustomPage
from datetime import datetime, date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import models


EXCLUDED_MODELS = ()


class ProjectMixin(DynamicContentMixin):

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)

        if not isinstance(self.object, Project):
            self.project = self.object.project
        else:
            self.project = self.object

        department = None

        if self.project.lead_team:
            if self.project.lead_team.department:
                department = self.project.lead_team.department
        else:
            for team in self.project.teams.all():
                if team.department:
                    department = team.department
                    break

        context['department'] = department
        if self.project.topic and self.project.topic.parent:
            context['page'] = self.project.topic.parent.pages.all().first()
        elif self.project.topic:
            context['page'] = self.project.topic.pages.all().first()

        return context


class ProjectDetailView(SlugMixin, ProjectMixin, DetailView):

    model = Project
    template_name='projects/project_detail.html'


class ProjectTechDetailView(SlugMixin, ProjectMixin, DetailView):

    model = Project
    template_name='projects/project_ict_detail.html'
    topic_key = 'ICT'

    def get_object(self, queryset=None):
        topic, c = ProjectTopic.objects.get_or_create(key=self.topic_key)
        project = super(ProjectTechDetailView, self).get_object()
        if project.topic != topic:
            raise Http404()
        return project


class ProjectListView(ListView):

    model = Project
    template_name='projects/project_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectListView, self).get_context_data(*args, **kwargs)
        project_list = []
        project_list.append({'title': 'Available projects', 'objects': Project.objects.filter(validation_status=3).order_by('title')})
        project_list.append({'title': 'Ongoing projects', 'objects': Project.objects.filter(validation_status=4).order_by('title')})
        project_list.append({'title': 'Other projects', 'objects': Project.objects.filter(validation_status=5).order_by('title')})
        context['project_list'] = project_list
        return context


class DynamicContentProjectView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        persons = Person.objects.all()
        organizations = Organization.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            persons = persons.filter(title__icontains=self.q)
            organizations = organizations.filter(name__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events, persons, organizations)
        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class ProjectDemoDetailView(SlugMixin, ProjectMixin, DetailView):

    model = ProjectDemo
    template_name='projects/project_demo_detail.html'
    context_object_name = 'demo'


class ProjectBlogPageView(SlugMixin, ProjectMixin, DetailView):

    model = ProjectBlogPage
    template_name='projects/project_blogpage_detail.html'


class ProjectCallMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ProjectCallMixin, self).get_context_data(**kwargs)
        self.call = ProjectCall.objects.get(slug=self.kwargs['call_slug'])
        context['call'] = self.call
        return context


class ProjectTechSubmissionView(ProjectCallMixin, TemplateView):

    model = Project
    template_name='projects/project_ict_submission.html'


class ProjectTechCreateView(LoginRequiredMixin, ProjectCallMixin, CreateWithInlinesView):

    model = Project
    form_class = ProjectForm
    topic_key = 'ICT'

    def get_inlines(self):
        if self.kwargs['funding'] == 'public':
            return [ProjectPublicDataInline, ProjectPrivateDataPublicFundingInline,
                ProjectUserImageInline, ProjectContactInline]
        elif self.kwargs['funding'] == 'private':
            return [ProjectPublicDataInline, ProjectPrivateDataPrivateFundingInline,
                ProjectUserImageInline, ProjectContactInline]

    def get_template_names(self):
        return ['projects/project_ict_create_%s_funding.html' % self.kwargs['funding']]

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.call = ProjectCall.objects.get(slug=self.kwargs['call_slug'])
        self.object.call = self.call
        self.object.topic, c = ProjectTopic.objects.get_or_create(key=self.topic_key)
        self.status = 1
        self.object.funding = self.kwargs['funding']
        self.object.save()
        return super(ProjectTechCreateView, self).forms_valid(form, inlines)

    def get_success_url(self):
        if 'save' in self.request.POST:
            return reverse_lazy('organization-network-profile-applications')
        elif 'submit' in self.request.POST:
            return reverse_lazy('organization-call-project-validate',
                kwargs={'call_slug': self.object.call.slug, 'slug': self.object.slug})
        else:
            return reverse_lazy('organization-network-profile-applications')


class ProjectTechUpdateView(LoginRequiredMixin, ProjectCallMixin, UpdateWithInlinesView):

    model = Project
    form_class = ProjectForm

    def get_inlines(self):
        if self.object.funding == 'public':
            return [ProjectPublicDataInline, ProjectPrivateDataPublicFundingInline,
                ProjectUserImageInline, ProjectContactInline]
        elif self.object.funding == 'private':
            return [ProjectPublicDataInline, ProjectPrivateDataPrivateFundingInline,
                ProjectUserImageInline, ProjectContactInline]

    def get_template_names(self):
        return ['projects/project_ict_edit_%s_funding.html' % self.object.funding]

    def get_initial(self):
        initial = super(ProjectTechUpdateView, self).get_initial()
        slug = self.kwargs['slug']
        user = self.request.user
        project = Project.objects.get(slug=slug)
        if project:
            if project.user == user:
                initial['title'] = project.title
                initial['website'] = project.website
                initial['date_from'] = project.date_from
                initial['date_to'] = project.date_to
                initial['keywords'] = project.keywords.all()
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectTechUpdateView, self).get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']
        user = self.request.user
        project = Project.objects.get(slug=slug)
        context["project"] = project
        context["public_data"] = project.public_data.all().first()
        context["private_data"] = project.private_data.all().first()
        context["keywords"] = project.keywords.all()
        if not project or project.user != user:
            raise Http404()
        return context

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super(ProjectTechUpdateView, self).forms_valid(form, inlines)

    def get_success_url(self):
        if 'save' in self.request.POST:
            return reverse_lazy('organization-network-profile-applications')
        elif 'submit' in self.request.POST:
            return reverse_lazy('organization-call-project-validate',
                kwargs={'call_slug': self.object.call.slug, 'slug': self.object.slug})
        else:
            return reverse_lazy('organization-network-profile-applications')


class ProjectTechValidateView(ProjectCallMixin, TemplateView):

    model = Project
    template_name='projects/project_ict_validation.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectTechValidateView, self).get_context_data(*args, **kwargs)
        project = Project.objects.get(slug=kwargs['slug'])
        project.validation_status = 2
        project.save()

        contacts = project.contacts.all()
        if contacts:
            contact = contacts[0]

            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_TO_EMAIL]
            if contact.email:
                to_email.append(contact.email)
            if self.request.user.email:
                to_email.append(self.request.user.email)
            subject = settings.EMAIL_SUBJECT_PREFIX + ' ' + project.call.title
            ctx = {
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'project_title': project.title,
            }

            message = get_template('projects/project_ict_create_notification.html').render(Context(ctx))
            msg = EmailMessage(subject, message, to=to_email, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

        return context


class ProjectTechListCallView(ListView):

    model = Project
    template_name='projects/project_ict_list.html'

    def get_queryset(self):
        topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        call = ProjectCall.objects.get(slug=self.kwargs['call_slug'])
        qs = Project.objects.filter(topic=topic, validation_status=3,
                call=call).select_related().order_by('title')
        return qs


class ProjectCallDetailView(SlugMixin, DetailView):

    model = ProjectCall
    template_name='projects/project_call_detail.html'


class ProjectCallListView(ListView):

    model = ProjectCall
    template_name='projects/project_call_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCallListView, self).get_context_data(*args, **kwargs)
        context["open_calls"] = ProjectCall.objects.filter(date_to__gte=datetime.now()).order_by("date_to")
        context["closed_calls"] = ProjectCall.objects.filter(date_to__lt=datetime.now()).order_by("date_to")
        return context


class ProjectCallListAsEventsView(ProjectCallListView):

    template_name = "projects/project_call_list_as_events.html"



class ProjectResidencyDetailView(SlugMixin, DetailView):

    model = ProjectResidency
    template_name='projects/project_residency_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectResidencyDetailView, self).get_context_data(**kwargs)
        # Add the previous and next residencies to the context
        call = ProjectCall.objects.get(slug=self.kwargs["call_slug"])
        projects = Project.objects.filter(call=call)
        residencies = ProjectResidency.objects.filter(project__in=projects, validated=True).select_related().order_by("id")
        this_residency = residencies.get(slug=self.kwargs["slug"])
        index = 0
        for i, residency in enumerate(residencies):
            if residency == this_residency:
                index = i
                break
        context["previous_residency"] = residencies[(index - 1) % len(residencies)]
        context["next_residency"] = residencies[(index + 1) % len(residencies)]
        return context


class ProjectResidencyListView(ListView):

    model = ProjectResidency
    template_name='projects/project_residency_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectResidencyListView, self).get_context_data(**kwargs)

        # Add the Call to the context
        if 'call_slug' in self.kwargs:
            context["call"] = ProjectCall.objects.get(slug=self.kwargs["call_slug"])

        # Add the related Keywords to the context
        keywords = []
        for residency in context["object_list"]:
            for keyword in residency.keywords.all():
                if keyword not in keywords:
                    keywords.append(keyword)
        context["keywords"] = keywords
        return context

    def get_queryset(self):
        if 'call_slug' in self.kwargs:
            call = ProjectCall.objects.get(slug=self.kwargs["call_slug"])
            projects = Project.objects.filter(call=call)
        else:
            projects = Project.objects.all()
        qs = ProjectResidency.objects.filter(project__in=projects, validated=True).select_related().order_by("id")
        if not self.request.user.is_superuser:
            qs = qs.filter(status=2)
        return qs


class ProjectResidencyCreateView(CreateWithInlinesView):

    model = ProjectResidency
    form_class = ProjectResidencyForm
    template_name='projects/project_residency_create.html'
    inlines = []
