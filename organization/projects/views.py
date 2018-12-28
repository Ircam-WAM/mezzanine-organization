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

from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin
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
from organization.core.views import *
from organization.magazine.views import Article
from organization.pages.models import CustomPage
from datetime import datetime, date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from guardian.mixins import *
from django.core.exceptions import PermissionDenied


class ProjectMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        self.object = self.get_object()
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


class ProjectDetailView(PermissionRequiredMixin, SlugMixin, ProjectMixin, DetailView):

    model = Project
    template_name='projects/project_detail.html'
    permission_required = 'organization-projects.view_project'
    raise_exception = True  # Or else: endless loop if user hasn't the permission (project (not logged in) > auth > project (not authorized) > auth > ...)
    return_403 = True

    def check_permissions(self, request):
        '''
        Private project = check view permission
        Public project = do not check view permission
        '''
        requested_object  = self.get_object()

        if not requested_object.is_private:
            pass
        else:
            forbidden = False
            try:
                super().check_permissions(request)
            except PermissionDenied:
                forbidden = True
            if forbidden:
                raise PermissionDenied()


class ProjectICTDetailView(SlugMixin, ProjectMixin, DetailView):

    model = Project
    template_name='projects/project_ict_detail.html'

    def get_object(self, queryset=None):
        topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        project = super(ProjectICTDetailView, self).get_object()
        if project.topic != topic:
            raise Http404()
        #TODO: Check if user is registered and admin or creator to allow other status values
        if project.validation_status != 3:
            raise Http404()
        return project


class ProjectListView(ListView):

    model = Project
    template_name='projects/project_list.html'


class DynamicContentProjectView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events,)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

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
        self.call = ProjectCall.objects.get(slug=self.kwargs['slug'])
        context['call'] = self.call
        return context


class ProjectICTSubmissionView(ProjectCallMixin, TemplateView):

    model = Project
    template_name='projects/project_ict_submission.html'


class ProjectICTCreateView(LoginRequiredMixin, ProjectCallMixin, CreateWithInlinesView): # pragma: no cover

    model = Project
    form_class = ProjectForm
    template_name='projects/project_ict_create.html'
    inlines = [ProjectPublicDataInline, ProjectPrivateDataInline, ProjectUserImageInline,
                ProjectContactInline]
    topic = 'ICT'
    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.call = ProjectCall.objects.get(slug=self.kwargs['slug'])
        self.object.call = self.call
        self.object.topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        self.status = 1
        self.object.save()

        for formset in inlines:
            if 'contact' in formset.prefix:
                for f in formset:
                    contact_data = f.cleaned_data
                    contact_email = contact_data.get("email")

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [contact_email, settings.DEFAULT_TO_EMAIL]
        subject = settings.EMAIL_SUBJECT_PREFIX + ' ' + self.call.title
        ctx = {
            'first_name': contact_data['first_name'],
            'last_name': contact_data['last_name'],
            'project_title': self.object.title,
        }

        message = get_template('projects/project_ict_create_notification.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to_email, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

        return super(ProjectICTCreateView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('organization-project-validation', kwargs={'slug':self.call.slug})


class ProjectICTCreatePublicFundingView(LoginRequiredMixin, ProjectCallMixin, CreateWithInlinesView):

    model = Project
    form_class = ProjectForm
    template_name='projects/project_ict_create_public_funding.html'
    inlines = [ProjectPublicDataInline, ProjectPrivateDataPublicFundingInline, ProjectUserImageInline,
                ProjectContactInline]
    topic = 'ICT'

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.call = ProjectCall.objects.get(slug=self.kwargs['slug'])
        self.object.call = self.call
        self.object.topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        self.status = 1
        self.object.funding = "public"
        self.object.save()

        for formset in inlines:
            if 'contact' in formset.prefix:
                for f in formset:
                    contact_data = f.cleaned_data
                    contact_email = contact_data.get("email")

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [contact_email, settings.DEFAULT_TO_EMAIL]
        subject = settings.EMAIL_SUBJECT_PREFIX + ' ' + self.call.title
        ctx = {
            'first_name': contact_data.get("first_name"),
            'last_name': contact_data.get("last_name"),
            'project_title': self.object.title,
        }

        message = get_template('projects/project_ict_create_notification.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to_email, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
        return super(ProjectICTCreatePublicFundingView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('organization-project-validation', kwargs={'slug':self.call.slug})

class ProjectICTEditPublicFundingView(LoginRequiredMixin, UpdateWithInlinesView):

    model = Project
    form_class = ProjectForm
    template_name='projects/project_ict_edit_public_funding.html'
    inlines = [ProjectPublicDataInline, ProjectPrivateDataPublicFundingInline, ProjectUserImageInline,
                ProjectContactInline]

    def get_initial(self):
        initial = super(ProjectICTEditPublicFundingView, self).get_initial()
        slug = self.kwargs['slug']
        user = self.request.user
        project = Project.objects.get(slug=slug)
        if project:
            if project.user == user:
                initial['title'] = project.title
                initial['website'] = project.website
                initial['date_from'] = project.date_from
                initial['date_to'] = project.date_to
        return initial

    def get_context_data(self, **kwargs):
        context = super(ProjectICTEditPublicFundingView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        user = self.request.user
        project = Project.objects.get(slug=slug)
        if (not project) or (project.user != user):
            raise Http404()
        if (project.validation_status != 1):
            raise Http404()
        context["project"] = project
        context["public_data"] = project.public_data.all().first()
        context["private_data"] = project.private_data.all().first()
        context["keywords"] = ""
        try:
            if project.contacts.all().count() > 0:
                contacts = project.contacts.all().first()
                context["contacts"] = contacts
                if contacts.keywords.all().count() > 0:
                    index = 0
                    keywords_result = ""
                    for key in contacts.keywords.all():
                        if index == 0:
                            keywords_result = keyword
                        elif index <= 2 and index > 0:
                            keywords_result = "," + keyword
                        else:
                            break
                    context["keywords"] = keywords_result
                else:
                    context["keywords"] = ""
            else:
                context["keywords"] = ""
        except Exception:
            pass
        return context

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super(ProjectICTEditPublicFundingView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('user-project-edit', kwargs={'slug':self.call.slug})


class ProjectICTCreatePrivateFundingView(LoginRequiredMixin, ProjectCallMixin, CreateWithInlinesView):

    model = Project
    form_class = ProjectForm
    template_name='projects/project_ict_create_private_funding.html'
    inlines = [ProjectPublicDataInline, ProjectPrivateDataPrivateFundingInline, ProjectUserImageInline,
                ProjectContactInline]
    topic = 'ICT'

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.call = ProjectCall.objects.get(slug=self.kwargs['slug'])
        self.object.call = self.call
        self.object.topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        self.status = 1
        self.object.funding = "private"
        self.object.save()

        for formset in inlines:
            if 'contact' in formset.prefix:
                for f in formset:
                    contact_data = f.cleaned_data
                    contact_email = contact_data.get("email")

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [contact_email, settings.DEFAULT_TO_EMAIL]
        subject = settings.EMAIL_SUBJECT_PREFIX + ' ' + self.call.title
        ctx = {
            'first_name': contact_data.get("first_name"),
            'last_name': contact_data.get("last_name"),
            'project_title': self.object.title,
        }

        message = get_template('projects/project_ict_create_notification.html').render(Context(ctx))
        msg = EmailMessage(subject, message, to=to_email, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
        return super(ProjectICTCreatePrivateFundingView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('organization-project-validation', kwargs={'slug':self.call.slug})


class ProjectICTEditPrivateFundingView(LoginRequiredMixin, UpdateWithInlinesView):

    model = Project
    form_class = ProjectForm
    template_name='projects/project_ict_edit_public_funding.html'
    inlines = [ProjectPublicDataInline, ProjectPrivateDataPublicFundingInline, ProjectUserImageInline,
                ProjectContactInline]
    def get_initial(self):
        initial = super(ProjectICTEditPrivateFundingView, self).get_initial()
        slug = self.kwargs['slug']
        user = self.request.user
        project = Project.objects.get(slug=slug)
        if project:
            if project.user == user:
                initial['title'] = project.title
                initial['website'] = project.website
                initial['date_from'] = project.date_from
                initial['date_to'] = project.date_to
        return initial

    def get_context_data(self, **kwargs):
        context = super(ProjectICTEditPrivateFundingView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        user = self.request.user
        project = Project.objects.get(slug=slug)
        if (not project) or (project.user != user):
            raise Http404()
        if (project.validation_status != 1):
            raise Http404()
        context["project"] = project
        context["public_data"] = project.public_data.all().first()
        context["private_data"] = project.private_data.all().first()
        context["keywords"] = ""
        try:
            if project.contacts.all().count() > 0:
                contacts = project.contacts.all().first()
                context["contacts"] = contacts
                if contacts.keywords.all().count() > 0:
                    index = 0
                    keywords_result = ""
                    for key in contacts.keywords.all():
                        if index == 0:
                            keywords_result = keyword
                        elif index <= 2 and index > 0:
                            keywords_result = "," + keyword
                        else:
                            break
                    context["keywords"] = keywords_result
                else:
                    context["keywords"] = ""
            else:
                context["keywords"] = ""
        except Exception:
            pass
        return context

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super(ProjectICTEditPrivateFundingView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('user-project-edit-private', kwargs={'slug':self.call.slug})


class ProjectICTValidationView(ProjectCallMixin, TemplateView):

    model = Project
    template_name='projects/project_ict_validation.html'


class ProjectICTListView(ListView):

    model = Project
    template_name='projects/project_ict_list.html'
    
    def get_queryset(self):
        topic, c = ProjectTopic.objects.get_or_create(key='ICT')
        #TODO: Filter by Call
        qs = Project.objects.filter(topic=topic).filter(validation_status=3).select_related().order_by('title')
        return qs


class ProjectCallDetailView(SlugMixin, DetailView):

    model = ProjectCall
    template_name='projects/project_call_detail.html'


class ProjectCallListView(ListView):

    model = ProjectCall
    template_name='projects/project_call_list.html'


class ProjectCallListAsEventsView(ListView):

    model = ProjectCall
    template_name = "projects/project_call_list_as_events.html"

    def get_context_data(self, *args, **kwargs):
        context = {}
        context["open_calls"] = ProjectCall.objects.filter(date_to__gte=datetime.now()).order_by("date_to")
        context["closed_calls"] = ProjectCall.objects.filter(date_to__lt=datetime.now()).order_by("date_to")
        return context


class ProjectResidencyDetailView(SlugMixin, DetailView):

    model = ProjectResidency
    template_name='projects/project_residency_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProjectResidencyDetailView, self).get_context_data(**kwargs)
        # Add the previous and next residencies to the context
        call = ProjectCall.objects.get(slug=self.kwargs["call_slug"])
        projects = Project.objects.filter(call=call)
        residencies = ProjectResidency.objects.filter(project__in=projects).filter(validated=True).select_related().order_by("id")
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
        call = ProjectCall.objects.get(slug=self.kwargs["call_slug"])
        projects = Project.objects.filter(call=call)
        qs = ProjectResidency.objects.filter(project__in=projects).filter(validated=True).select_related().order_by("id")
        return qs


class ProjectResidencyCreateView(CreateWithInlinesView):

    model = ProjectResidency
    form_class = ProjectResidencyForm
    template_name = 'projects/project_residency_create.html'
    inlines = []


class ProjectCollectionDetailView(DetailView):

    model = ProjectCollection
    template_name = 'projects/project_collection_detail.html'

    # Ordering by project title
    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCollectionDetailView, self).get_context_data(*args, **kwargs)
        context['collection'] = context['object']
        pp = context['collection'].projects_pivot.all().order_by('project__title')
        context['projects'] = [p.project for p in pp]
        return context


class ProjectCollectionListView(ListView):

    model = ProjectCollection
    template_name = 'projects/project_collection_list.html'


class ProjectTopicDetailView(DetailView):

    model = ProjectTopic
    template_name = 'projects/project_topic_detail.html'

    # def get_object(self):
    #     return get_object_or_404(ProjectTopic, pk=self.kwargs['id'])


class Pivot_Project_ProjectCollection_View(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        projects = Project.objects.all()

        if self.q:
            projects = projects.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(projects,)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

        return qs

    # def get_results(self, context):
    #     results = autocomplete_result_formatting(self, context)
    #     return results


class ProjectCreateView(LoginRequiredMixin, TemplateView):

    template_name = 'projects/project_creation.html'
    permission_required = 'organization-projects.add_project'


class ProjectEditView(PermissionRequiredMixin, LoginRequiredMixin, SlugMixin, DetailView):

    model = Project
    template_name = 'projects/project_edit.html'
    permission_required = 'organization-projects.change_project'
    raise_exception = True
    return_403 = True


class ProjectTopicAutocompleteView(autocomplete.Select2QuerySetView):

    from django.db.models import Q

    def get_result_label(self, item):
        return item.name

    def get_queryset(self):

        qs = ProjectTopic.objects.all()

        value = self.forwarded.get('value', None)

        if value:
            qs = qs.filter(value=value)

        if self.q:
            # For OR queries see https://docs.djangoproject.com/fr/2.0/topics/db/queries/#complex-lookups-with-q-objects
            qs = qs.filter(key__istartswith=self.q)

        return qs