from django.shortcuts import render
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from organization.network.models import *
from organization.core.views import *


class DepartmentListView(ListView):

    model = Department
    template_name='team/department_list.html'


class DepartmentDetailView(SlugMixin, DetailView):

    model = Department
    template_name='team/department_detail.html'
    context_object_name = 'department'


class TeamListView(ListView):

    model = Team
    template_name='team/team_list.html'


class TeamDetailView(SlugMixin, DetailView):

    model = Team
    template_name='team/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        partners = []

        for partner in self.object.partner_organizations:
            partners.append(partner)
        for partner in self.object.partner_teams:
            partners.append(partner)

        for project in team.project_leader.all():
            for partner in project.partner_organizations:
                partners.append(partner)
            for partner in project.partner_teams:
                partners.append(partner)

        context['partners'] = partners
        return context


class PersonListView(ListView):

    model = Person
    template_name='team/person_list.html'


class PersonDetailView(SlugMixin, DetailView):

    model = Person
    template_name='team/person_detail.html'
    context_object_name = 'person'


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
