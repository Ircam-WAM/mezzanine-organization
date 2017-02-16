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
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.forms import formset_factory
from django.http import HttpResponse
from mezzanine.conf import settings
from django.core.urlresolvers import reverse
from dal import autocomplete
from organization.network.models import *
from organization.core.views import *
from datetime import date
from organization.network.forms import *
from organization.network.utils import TimesheetXLS
from organization.projects.models import ProjectWorkPackage
from collections import OrderedDict
from django.http.response import HttpResponseRedirect


class PersonListView(ListView):

    model = Person
    template_name='team/person_list.html'


class PersonDetailView(SlugMixin, DetailView):

    model = Person
    template_name='network/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context["person_email"] = self.object.email if self.object.email else self.object.slug.replace('-', '.')+" (at) ircam.fr"
        return context


class PersonListBlockAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        # if not self.request.is_authenticated():
        #     return PersonListBlock.objects.none()

        qs = PersonListBlock.objects.all()

        title = self.forwarded.get('title', None)

        if title:
            qs = qs.filter(title=title)

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs


class PersonListView(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Person.objects.all()

        person_title = self.forwarded.get('person_title', None)

        if person_title:
            qs = qs.filter(person_title=person_title)

        if self.q:
            qs = qs.filter(person_title__istartswith=self.q)

        return qs

class OrganizationListView(ListView):

    model = Organization
    context_object_name = 'organizations'
    template_name='network/organization_list.html'

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(is_on_map=True)

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context['organization_types'] = self.get_queryset().values_list('type__name', 'type__css_class').order_by('type__name').distinct('type__name')
        return context


class OrganizationLinkedListView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = OrganizationLinked.objects.all()
        orga_linked_title = self.forwarded.get('title', None)
        if orga_linked_title:
            qs = qs.filter(title=orga_linked_title)
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs


class OrganizationLinkedView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Organization.objects.all()
        orga_name= self.forwarded.get('name', None)
        if orga_name:
            qs = qs.filter(name=orga_name)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs



class TimesheetAbstractView(LoginRequiredMixin):
    login_url = settings.LOGIN_URL

    class Meta:
        abstract = True


class TimeSheetCreateView(TimesheetAbstractView, CreateView):
    model = PersonActivityTimeSheet
    template_name='network/person_activity_timesheet/person_activity_timesheet_create.html'
    context_object_name = 'timesheet'
    fields = '__all__'
    formset = ""
    PersonActivityTimeSheetFormSet = formset_factory(PersonActivityTimeSheetForm, extra=0)

    def get_activity_by_project(self, slug, year, month):
        project_list = []
        activity = PersonActivity.objects.filter(person__slug=slug).first()
        for project_activity in activity.project_activity.all() :
            project_list.append({
                'activity' : activity,
                'project' : project_activity.project,
                'work_packages' : project_activity.work_packages.all(),
                'year' : year,
                'month' : month,
                'percentage' : project_activity.default_percentage
            })
        return project_list

    def get(self, request, *args, **kwargs):
        project_list = self.get_activity_by_project(self.kwargs['slug'], self.kwargs['year'], self.kwargs['month'])
        self.formset = self.PersonActivityTimeSheetFormSet(initial=project_list)
        return render(request, 'network/person_activity_timesheet/person_activity_timesheet_create.html', {'formset': self.formset})

    def post(self, request, *args, **kwargs):
        self.formset = self.PersonActivityTimeSheetFormSet(request.POST)
        errors = []
        if self.formset.is_valid():
            for form in self.formset:
                form.save()
            return HttpResponseRedirect(reverse('organization-network-timesheet-list-view', kwargs={'slug': self.kwargs['slug']}))
        else :
            errors = self.formset.errors
            project_list = self.get_activity_by_project(self.kwargs['slug'], self.kwargs['year'], self.kwargs['month'])
            self.formset = self.PersonActivityTimeSheetFormSet(initial=project_list)

        return render(request, 'network/person_activity_timesheet/person_activity_timesheet_create.html', {'formset': self.formset, 'errors' : errors, 'slug': self.kwargs['slug']})

    def get_success_url(self):
        return reverse('organization-network-timesheet-list-view', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(TimeSheetCreateView, self).get_context_data(**kwargs)
        context.push(self.formset)
        context.push(self.kwargs)
        return context

    def form_valid(self, form):
        messages.info(self.request, _("You have successfully submitted your timsheet."))
        return super(TimeSheetCreateView, self).form_valid(form)


class PersonActivityTimeSheetListView(TimesheetAbstractView, ListView):
    model = PersonActivityTimeSheet
    template_name='network/person_activity_timesheet/person_activity_timesheet_list.html'
    context_object_name = 'timesheets_by_year'

    def get_queryset(self):
        if 'slug' in self.kwargs:
            timesheets = PersonActivityTimeSheet.objects.filter(activity__person__slug__exact=self.kwargs['slug'])
            t_dict = OrderedDict()
            for timesheet in timesheets:
                year = timesheet.year
                if not year in t_dict:
                    t_dict[year] = {}
                project_slug = timesheet.project.title
                # if new person
                if not project_slug in t_dict[year]:
                    t_dict[year][project_slug] = []
                t_dict[year][project_slug].append(timesheet)
            return t_dict

    def get_context_data(self, **kwargs):
        context = super(PersonActivityTimeSheetListView, self).get_context_data(**kwargs)
        context['current_month'] = date.today().month
        context['current_year'] = date.today().year
        context.update(self.kwargs)
        return context


class PersonActivityTimeSheetExportView(TimesheetAbstractView, View):

    def get(self, *args, **kwargs):
        timesheets = PersonActivityTimeSheet.objects.filter(activity__person__slug__exact=kwargs['slug'], year=kwargs['year'])
        xls = TimesheetXLS(timesheets)
        return xls.write()


def fetch_work_packages(request, **kwargs):
    work_packages = ProjectWorkPackage.objects.filter(project_id=kwargs['project_id'])
    return HttpResponse(work_packages)
