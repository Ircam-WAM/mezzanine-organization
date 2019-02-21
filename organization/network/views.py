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
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import View
from django.forms import formset_factory, BaseFormSet
from extra_views import FormSetView
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _
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
from django.utils import six
from django.core.exceptions import PermissionDenied
from organization.pages.forms import YearForm
from organization.pages.views import PublicationsView

import pandas as pd


class PersonMixin(object):

    model = Person

    def get_object(self, queryset=None):
        person = None
        user = self.request.user
        if user.is_authenticated():
            if not Person.objects.filter(user=user):
                person = Person(first_name=user.first_name, last_name=user.last_name, user=user,
                                email=user.email, title=' '.join([user.first_name, user.last_name]))
                person.save()
            person = user.person

        if 'username' in self.kwargs:
            users = User.objects.filter(username=self.kwargs['username'])
            if users:
                user = users[0]
                person = user.person

        elif 'slug' in self.kwargs:
            persons = Person.objects.filter(slug=self.kwargs['slug'])
            if persons:
                person = persons[0]

        try:
            person.title
        except AttributeError:
            raise Http404("This person does not exist")

        return person

    @property
    def person(self):
        if 'username' in self.kwargs:
            user = User.objects.get_object_or_404(username=self.kwargs['username'])
        else:
            user = self.request.user
        return user.person


class PersonListView(PublishedMixin, ListView):

    model = Person
    template_name='network/person_list.html'
    context_object_name = 'persons'


class PersonDirectoryView(ListView):
    
    model = Person
    template_name='network/person/directory.html'
    context_object_name = 'persons'
    ordering = "last_name"
    letter = "letter"

    def get_queryset(self):
        self.queryset = super(PersonDirectoryView, self).get_queryset()
        if not self.kwargs['letter']:
            self.kwargs['letter'] = "a"
        self.queryset = self.queryset.filter(Q(last_name__istartswith=self.kwargs['letter'])
                                            & Q(activities__date_to__gte=datetime.date.today())
                                            & Q(activities__umr=1)).distinct()
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(PersonDirectoryView, self).get_context_data(**kwargs)
        letters_pagination = OrderedDict()

        # list all letters from a (97) to z (123)
        for c in range(97, 123):
            letters_pagination[chr(c)] = reverse_lazy('person-directory', kwargs={'letter': chr(c)})
        context['letters_pagination'] = letters_pagination
        context['curr_letter'] = self.kwargs['letter']
        return context


class TeamMembersView(ListView):
    
    model = Person
    template_name='network/team/members.html'
    context_object_name = 'persons'
    permanents = []
    non_permanents = []
    old_members = [] 

    def get_queryset(self):
        self.permanents = []
        self.non_permanents = []
        self.old_members = []
        self.queryset = super(TeamMembersView, self).get_queryset()
        
        # Filter by Team, distinct on Person
        lookup = Q(activities__teams__slug=self.kwargs['slug'])
        self.queryset = self.queryset.filter(lookup) \
                                        .order_by("last_name", "first_name") \
                                        .distinct("last_name", "first_name")

        # Filter active persons
        lookup = lookup & Q(activities__date_to__gte=datetime.date.today())
        active_persons = self.queryset.filter(lookup)

        # permanent persons
        permanent_person = active_persons.filter(lookup & Q(activities__is_permanent=True))
        # Filter Head Researcher
        head_researcher = ""
        for p in permanent_person:
            if hasattr(p.activities.first().status, 'id') and p.activities.first().status.id == 6 : #Head Researcher
                head_researcher = p
            else :
                self.permanents.append(p)

        # add Head Researcher at first place
        if head_researcher:
            self.permanents.insert(0, head_researcher)
        

        # non permanent persons
        permanent_persons_id = [p.id for p in permanent_person]
        self.non_permanents = active_persons.filter(lookup & Q(activities__is_permanent=False)) \
                                            .exclude(id__in=permanent_persons_id)

        
        # former persons  
        active_persons_id = [p.id for p in active_persons]
        self.old_members = self.queryset.filter(Q(activities__teams__slug=self.kwargs['slug']) \
                                                & Q(activities__date_to__lt=datetime.date.today())) \
                                        .exclude(id__in=active_persons_id)

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(TeamMembersView, self).get_context_data(**kwargs)
        context['permanents'] = self.permanents
        context['non_permanents'] = self.non_permanents
        context['old_members'] = self.old_members
        context['team'] = Team.objects.get(slug=self.kwargs['slug'])
        return context


class TeamPublicationsView(PublicationsView):
    
    template_name = "network/team/publications.html"
    team = None

    def get(self, request, *args, **kwargs):
        self.team = get_object_or_404(Team, slug=kwargs['slug'])
        self.hal_url += "&" + settings.HAL_LABOS_EXP + "%s" % self.team.hal_researche_structure.replace(' ', '+')
        return super(TeamPublicationsView, self).get(request, *args, **kwargs)


class PersonDetailView(PersonMixin, SlugMixin, DetailView):

    model = Person
    template_name='network/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context["related"] = {}
        # Related Events when you add PersonList in Events
        events = []
        if hasattr(self.object, "person_list_block_inlines"):
            person_list_block_inlines = self.object.person_list_block_inlines.all()
            for plbi in person_list_block_inlines:
                if hasattr(plbi.person_list_block, 'events'):
                    for eventPersonListBlockInline in plbi.person_list_block.events.all():
                        events.append(eventPersonListBlockInline.event)
        context["related"]["event"] = events

        # All other related models
        context["related"]["other"] = []
        # for each person list to which the person belongs to...
        for person_list_block_inline in person_list_block_inlines:
            if hasattr(person_list_block_inline, 'person_list_block_inline') :
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
                                        if not isinstance(instance, person_list_block_inline.person_list_block.__class__) and instance:  #and not isinstance(person_list_block_inline.person_list_block.__class__):
                                            context["related"]["other"].append(instance)

        context["related"]["other"].sort(key=lambda x: x.created, reverse=True)
        context["person_email"] = self.object.email if self.object.email else self.object.slug.replace('-', '.')+" (at) ircam.fr"
        return context


class PersonListBlockAutocompleteView(autocomplete.Select2QuerySetView):

    def get_result_label(self, result):
        """Return the label of a result."""
        label = result.label if result.label else "..."
        return six.text_type(label + " - " + result.__str__())

    def get_queryset(self):

        qs = PersonListBlock.objects.all()

        label = self.forwarded.get('label', None)

        if label:
            qs = qs.filter(label=label)

        if self.q:
            qs = qs.filter(label__istartswith=self.q)

        return qs


class PersonAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Person.objects.all()

        person_title = self.forwarded.get('title', None)

        if person_title:
            qs = qs.filter(title=person_title)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

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


class ProducerDetailView(SlugMixin, DetailView):

    model = Organization
    template_name='network/organization_producer_detail.html'

    def get_object(self, queryset=None):
        role, c = OrganizationRole.objects.get_or_create(key='Producer')
        producer = super(ProducerDetailView, self).get_object()
        if producer.role != role:
            raise Http404()
        #TODO: Check if user is registered and admin or creator to allow other status values
        if producer.validation_status != 3:
            raise Http404()
        return producer


class ProducerListView(ListView):

    model = Organization
    template_name='network/organization_producer_list.html'

    def get_queryset(self):
        role, c = OrganizationRole.objects.get_or_create(key='Producer')
        qs = Organization.objects.filter(role=role).filter(validation_status=3).select_related().order_by('name')
        return qs


class ProducerCreateView(LoginRequiredMixin, CreateWithInlinesView):

    model = Organization
    form_class = ProducerForm
    template_name='network/organization_producer_create.html'
    inlines = [ProducerDataInline]

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.role, c = OrganizationRole.objects.get_or_create(key='Producer')
        self.object.save()
        return super(ProducerCreateView, self).forms_valid(form, inlines)

    def get_success_url(self):
        #TODO: When logging system is implemented, maybe use this instead
        # return reverse_lazy('organization-producer-detail', kwargs={'slug':self.object.slug})
        return reverse_lazy('organization-producer-validation', kwargs={'slug':self.object.slug})


class ProducerValidationView(ProducerMixin, TemplateView):

    model = Organization
    template_name='network/organization_producer_validation.html'


class TimesheetAbstractView(LoginRequiredMixin):
    login_url = settings.LOGIN_URL

    class Meta:
        abstract = True


class TimeSheetCreateView(TimesheetAbstractView, FormSetView): # pragma: no cover
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

    def get(self, request, *args, **kwargs):
        # the user can create a timesheet only month-1..n
        if 'year' in kwargs and 'month' in kwargs:
            curr_date = datetime.date.today()
            asked_date = date(int(kwargs['year']), int(kwargs['month']), curr_date.day)
            if (curr_date - asked_date).days <= 0:
                raise PermissionDenied

        return super(TimeSheetCreateView, self).get(request, *args, **kwargs)

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
            for project_activity in activity.project_activity.filter(project__date_to__gte=last_day_in_month) :
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


class PersonActivityTimeSheetListView(TimesheetAbstractView, ListView): # pragma: no cover
    model = PersonActivityTimeSheet
    template_name='network/person_activity_timesheet/person_activity_timesheet_list.html'
    context_object_name = 'timesheets_by_year'

    def get_queryset(self):

        # get list of months / years
        dt1 = date.today().replace(day=1)
        prev_month = dt1 - timedelta(days=1)
        timesheet_range = pd.date_range(settings.TIMESHEET_START, prev_month, freq="MS")
        timesheets = PersonActivityTimeSheet.objects.filter(activity__person=self.request.user.person).order_by('-year', 'month', 'project')

        # construct timesheets table
        t_dict = {}

        for timesheet_date in timesheet_range:
            year = timesheet_date.year
            month = timesheet_date.month
            if not year in t_dict:
                t_dict[year] = {}
                t_dict[year]['project_count'] = 0
                t_dict[year]['timesheets'] = {}

            if not month in t_dict[year]['timesheets']:
                t_dict[year]['timesheets'][month] = []

            timesheet = [t for t in timesheets if t.month == timesheet_date.month and t.year == timesheet_date.year]
            if timesheet:
                t_dict[year]['timesheets'][month] += timesheet

            t_dict[year]['project_count'] = max(t_dict[year]['project_count'], len(t_dict[year]['timesheets'][month]))

        return OrderedDict(sorted(t_dict.items(), key=lambda t: -t[0]))

    def get_context_data(self, **kwargs):
        last_day_in_month = date.today().replace(day=1) - timedelta(days=1)
        context = super(PersonActivityTimeSheetListView, self).get_context_data(**kwargs)
        context['current_month'] = last_day_in_month.month
        context['current_year'] = last_day_in_month.year
        context['months'] = list(range(1, last_day_in_month.month + 1))
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


class PersonActivityAutocompleteView(autocomplete.Select2QuerySetView):

    def get_result_label(self, item):
        return item.person.first_name + ' ' + item.person.last_name + "  -  " + item.__str__()

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return PersonActivity.objects.none()

        qs = PersonActivity.objects.all()

        person_ln = self.forwarded.get('person__last_name', None)

        if person_ln:
            qs = qs.filter(person__last_name=person_ln)

        if self.q:
            qs = qs.filter(person__last_name__istartswith=self.q)

        return qs



class WorkPackageAutocompleteView(autocomplete.Select2QuerySetView):# ModelSelect2Multiple

    def get_result_label(self, item):
        return item.project.title + ' - ' + item.title

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return ProjectWorkPackage.objects.none()

        qs = ProjectWorkPackage.objects.all()

        project_title = self.forwarded.get('project__title', None)

        if project_title:
            qs = qs.filter(project__title=project_title)

        if self.q:
            qs = qs.filter(project__title__istartswith=self.q)

        return qs


class JuryListView(ListView):

    model = Person
    template_name="network/organization_jury_list.html"
    context_object_name = "jury"

    def get_context_data(self, **kwargs):
        context = super(JuryListView, self).get_context_data(**kwargs)
        context["description"] = ""
        jury_list = PersonListBlock.objects.filter(title__in=["Jury", "jury"])
        if jury_list:
            jury = jury_list[0]
            context["description"] = jury.description
        context.update(self.kwargs)
        return context

    def get_queryset(self):
        jury_list = PersonListBlock.objects.filter(title__in=["Jury", "jury"])
        if jury_list:
            jury = jury_list[0]
            qs = Person.objects.filter(person_list_block_inlines__person_list_block=jury).order_by("last_name")
        else:
            qs = Person.objects.none()

