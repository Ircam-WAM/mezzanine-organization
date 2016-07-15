from django.shortcuts import render

from organization.team.models import *
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


class PersonListView(ListView):

    model = Person
    template_name='team/person_list.html'


class PersonDetailView(SlugMixin, DetailView):

    model = Person
    template_name='team/person_detail.html'
    context_object_name = 'person'
