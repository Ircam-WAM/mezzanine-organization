from django.shortcuts import render

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
