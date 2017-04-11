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

from re import match
from django.contrib import messages
from pprint import pprint
from calendar import monthrange
from django.db.models.fields.related import ForeignKey
from django.http import Http404
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import View
from django.forms import formset_factory, BaseFormSet
from extra_views import FormSetView
from django.http import HttpResponse
from mezzanine.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from dal import autocomplete
from organization.network.models import *
from organization.core.views import *
from datetime import date
from organization.network.forms import *
from organization.network.utils import TimesheetXLS
from organization.projects.models import ProjectWorkPackage
from collections import OrderedDict
from django.http.response import HttpResponseRedirect
from django.views.generic.base import RedirectView


class PersonListView(ListView):

    model = Person
    template_name='team/person_list.html'


class PersonDetailView(SlugMixin, DetailView):

    model = Person
    template_name='network/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context["related"] = {}
        # Person events : this type is separated from the other because
        # this is not managed by list of person by person in inlines directly
        person_events = self.object.events.all()
        events = [item.event for item in person_events]
        context["related"]["event"] = events
        # All other related models
        person_list_block_inlines = self.object.person_list_block_inlines.all()
        context["related"]["other"] = []
        # for each person list to which the person belongs to...
        for person_list_block_inline in person_list_block_inlines:
            related_objects = person_list_block_inline.person_list_block._meta.get_all_related_objects()
            for related_object in related_objects:
                if hasattr(person_list_block_inline.person_list_block, related_object.name):
                    # getting relating inlines like ArticlePersonListBlockInline, PageCustomPersonListBlockInline etc...
                    related_inlines = getattr(person_list_block_inline.person_list_block, related_object.name).all()
                    for related_inline in related_inlines:
                        if not isinstance(related_inline, person_list_block_inline.__class__):  #and not isinstance(person_list_block_inline.person_list_block.__class__):
                            fields = related_inline._meta.get_fields()
                            for field in fields:
                                # check if it is a ForeignKey
                                if isinstance(field, ForeignKey) :
                                    instance = getattr(related_inline, field.name)
                                    # get only article, custom page etc...
                                    if not isinstance(instance, person_list_block_inline.person_list_block.__class__) :  #and not isinstance(person_list_block_inline.person_list_block.__class__):
                                        context["related"]["other"].append(instance)

        context["related"]["other"].sort(key=lambda x: x.created, reverse=True)
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


class TimeSheetCreateView(TimesheetAbstractView, FormSetView):
    model = PersonActivityTimeSheet
    template_name='network/person_activity_timesheet/person_activity_timesheet_create.html'
    context_object_name = 'timesheet'
    fields = '__all__'
    form_class = PersonActivityTimeSheetForm
    formset = ""
    extra = 0
    success_url = reverse_lazy("organization-network-timesheet-list-view")
    curr_month = date.today().month
    curr_year = date.today().year

    def get_activity_by_project(self, email, year, month):
        project_list = []
        # backdoor to delete
        # activities = PersonActivity.objects.filter(person__slug=email).filter(date_to__gt=date.today())
        # if not activities :
        activities = PersonActivity.objects.filter(person__email=email).filter(date_to__gt=date.today())
        first_day_in_month = ''
        last_day_in_month = ''

        try :
            first_day_in_month = date(int(year), int(month), 1)
            last_day_in_month = date(int(year), int(month),  monthrange(int(year), int(month))[1])
        except ValueError:
            raise Http404

        # gather projects of all current activities
        for activity in activities:
            for project_activity in activity.project_activity.filter(project__date_to__gt=date.today()) :
                project_list.append({
                    'activity' : activity,
                    'project' : project_activity.project,
                    'work_packages' : project_activity.work_packages.filter(
                        Q(date_from__lte=first_day_in_month) & Q(date_to__gte=first_day_in_month)
                        | Q(date_from__gte=first_day_in_month) & Q(date_to__lte=last_day_in_month)
                        | Q(date_from__lte=last_day_in_month) & Q(date_to__gte=last_day_in_month)
                    ),
                    'year' : year,
                    'month' : month,
                    'percentage' : project_activity.default_percentage
                })
        return project_list

    def get_context_data(self, **kwargs):
        context = super(TimeSheetCreateView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        context['month'] = self.curr_month
        context['year'] = self.curr_year
        return context

    def get_initial(self):

        if "year" in self.kwargs:
            self.curr_year = self.kwargs['year']

        if "month" in self.kwargs:
            self.curr_month = self.kwargs['month']

        # if "slug" in self.kwargs:
        #     # backdoor to delete
        #     initial = self.get_activity_by_project(self.kwargs['slug'], self.curr_year, self.curr_month)
        # else :
        initial = self.get_activity_by_project(self.request.user.email, self.curr_year, self.curr_month)

        return initial

    def formset_valid(self, formset):
        is_valid = formset.is_valid()

        # check if TOTAL percentages do not exceed 100%
        percent = 0
        for data_k, data_v in formset.data.items():
            if match('form-\d+-percentage', data_k):
                percent += int(data_v)

        if percent > 100 :
            formset.errors.append( {'percentage': ['The total percentage worked do not have to exceed 100 %']})
            redirect = super(TimeSheetCreateView, self).formset_invalid(formset)
            is_valid = False

        for form in formset:
            form.instance.month = self.curr_month
            form.instance.year = self.curr_year
            try :
                form.save()
            except IntegrityError:
                is_valid = False
                formset.errors.append( {'Error': ['You already submitted this timesheet.']})


        if is_valid:
            redirect = super(TimeSheetCreateView, self).formset_valid(formset)
        else :
            redirect = super(TimeSheetCreateView, self).formset_invalid(formset)

        return redirect


class PersonActivityTimeSheetListView(TimesheetAbstractView, ListView):
    model = PersonActivityTimeSheet
    template_name='network/person_activity_timesheet/person_activity_timesheet_list.html'
    context_object_name = 'timesheets_by_year'

    def get_queryset(self):
       # if 'slug' in self.kwargs:
        #     # backdoor to delete
        #     timesheets = PersonActivityTimeSheet.objects.filter(activity__person__slug__exact=self.kwargs['slug']).order_by('-year', 'month', 'project')
        # else:
        timesheets = PersonActivityTimeSheet.objects.filter(activity__person__email__exact=self.request.user.email).order_by('-year', 'month', 'project')

        t_dict = {}
        for timesheet in timesheets:
            year = timesheet.year
            month = timesheet.month
            if not year in t_dict:
                t_dict[year] = {}
                t_dict[year]['project_count'] = 0
                t_dict[year]['timesheets'] = {}

            # if new person
            if not month in t_dict[year]['timesheets']:
                t_dict[year]['timesheets'][month] = []

            t_dict[year]['timesheets'][month].append(timesheet)
            t_dict[year]['project_count'] = max(t_dict[year]['project_count'], len(t_dict[year]['timesheets'][month]))

        # add manually current year if not exists
        curr_year = date.today().year
        if not curr_year in t_dict.keys():
            t_dict[curr_year] = {}
            t_dict[curr_year]['project_count'] = 0

        return OrderedDict(sorted(t_dict.items(), key=lambda t: -t[0]))

    def get_context_data(self, **kwargs):
        context = super(PersonActivityTimeSheetListView, self).get_context_data(**kwargs)
        context['current_month'] = date.today().month
        context['current_year'] = date.today().year
        context['months'] = list(range(1, date.today().month + 1))
        context.update(self.kwargs)
        return context


class PersonActivityTimeSheetExportView(TimesheetAbstractView, View):

    def get(self, *args, **kwargs):
        timesheets = PersonActivityTimeSheet.objects.filter(activity__person__slug__exact=kwargs['slug'], year=kwargs['year'])
        xls = TimesheetXLS(timesheets)
        return xls.write()


class TimeSheetCreateCurrMonthView(TimeSheetCreateView):
    pass


def fetch_work_packages(request, **kwargs):
    work_packages = ProjectWorkPackage.objects.filter(project_id=kwargs['project_id'])
    return HttpResponse(work_packages)
