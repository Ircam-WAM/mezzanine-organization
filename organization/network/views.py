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


class DynamicPersonListView(Select2QuerySetSequenceView):

    def get_queryset(self):
        persons = Person.objects.all()
        if self.q:
            persons = persons.filter(person_title__icontains=self.q)
        qs = autocomplete.QuerySetSequence(persons)
        if self.q:
            qs = qs.filter(person_title__icontains=self.q)
        qs = self.mixup_querysets(qs)
        return qs


class DynamicContentPersonListBlockView(Select2QuerySetSequenceView):

    def get_queryset(self):
        person_list_blocks = PersonListBlock.objects.all()
        if self.q:
            person_list_blocks = person_list_blocks.filter(title__icontains=self.q)
        qs = autocomplete.QuerySetSequence(person_list_blocks)
        if self.q:
            qs = qs.filter(title__icontains=self.q)
        qs = self.mixup_querysets(qs)
        return qs
