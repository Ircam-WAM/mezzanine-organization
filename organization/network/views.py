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
from datetime import date, timedelta, datetime
from organization.network.forms import *
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

    def get(self, request, *args, **kwargs):
        # if not hasattr(self.request.user, 'ldap_user') or not self.request.user.person:
        #     response = redirect('organization-home')
        self.object = self.get_object(self.queryset)
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        return response

    def get_object(self, queryset):
        obj = None
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
        else:
            slug = None

        if not slug and self.request.user.is_authenticated() and not 'username' in self.kwargs:
            obj = self.request.user.person
        elif 'username' in self.kwargs:
            user = User.objects.get(username=self.kwargs['username'])
            obj = Person.objects.get(user=user)
        else:
            obj = super().get_object()
        return obj

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context["person_email"] = self.object.email if self.object.email else self.object.slug.replace('-', '.')+" (at) ircam.fr"
        return context


class ProfileDetailView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'organization-network-person-detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_counter()
        return super(ArticleCounterRedirectView, self).get_redirect_url(*args, **kwargs)

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
    last_day_in_month = date.today().replace(day=1) - timedelta(days=1)
    curr_month = last_day_in_month.month
    curr_year = last_day_in_month.year

    def get_activity_by_project(self, user, year, month):
        project_list = []

        first_day_in_month = ''
        last_day_in_month = ''

        try :
            first_day_in_month = date(int(year), int(month), 1)
            last_day_in_month = date(int(year), int(month),  monthrange(int(year), int(month))[1])
        except ValueError:
            raise Http404

        activities = PersonActivity.objects.filter(person=user.person).filter(
            Q(date_from__lte=first_day_in_month) & Q(date_to__range=(first_day_in_month, last_day_in_month)) \
            | Q(date_from__range=(first_day_in_month, last_day_in_month)) & Q(date_to__range=(first_day_in_month, last_day_in_month)) \
            | Q(date_from__range=(first_day_in_month, last_day_in_month)) & Q(date_to__gte=last_day_in_month) \
            | Q(date_from__lte=first_day_in_month) & Q(date_to__gte=last_day_in_month) \
        )
        # gather projects of all current activities
        for activity in activities:
            for project_activity in activity.project_activity.filter(project__date_to__gt=date.today()) :
                project_list.append({
                    'activity' : activity,
                    'project' : project_activity.project,
                    'work_packages' : project_activity.work_packages.filter(
                        Q(date_from__lte=first_day_in_month) & Q(date_to__range=(first_day_in_month, last_day_in_month)) \
                        | Q(date_from__range=(first_day_in_month, last_day_in_month)) & Q(date_to__range=(first_day_in_month, last_day_in_month)) \
                        | Q(date_from__range=(first_day_in_month, last_day_in_month)) & Q(date_to__gte=last_day_in_month) \
                        | Q(date_from__lte=first_day_in_month) & Q(date_to__gte=last_day_in_month) \
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

        initial = self.get_activity_by_project(self.request.user, self.curr_year, self.curr_month)

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
        timesheets = PersonActivityTimeSheet.objects.filter(activity__person=self.request.user.person).order_by('-year', 'month', 'project')

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
        last_day_in_month = date.today().replace(day=1) - timedelta(days=1)
        context = super(PersonActivityTimeSheetListView, self).get_context_data(**kwargs)
        context['current_month'] = last_day_in_month.month
        context['current_year'] = last_day_in_month.year
        context['months'] = list(range(1, last_day_in_month.month + 1))
        context.update(self.kwargs)
        return context


class TimeSheetCreateCurrMonthView(TimeSheetCreateView):
    pass


def fetch_work_packages(request, **kwargs):
    work_packages = ProjectWorkPackage.objects.filter(project_id=kwargs['project_id'])
    return HttpResponse(work_packages)
