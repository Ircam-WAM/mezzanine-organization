from django.shortcuts import render

from organization.projects.models import *
from organization.core.views import *


class ProjectDetailView(SlugMixin, DetailView):

    model = Project
    template_name='projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        department = None

        if project.lead_team:
            if project.lead_team.department:
                department = project.lead_team.department
        else:
            for team in project.teams.all():
                if team.department:
                    department = team.department
                    break

        context['department'] = department
        if project.topic and project.topic.parent:
            context['page'] = project.topic.parent.pages.all().first()
        elif project.topic:
            context['page'] = roject.topic.pages.all().first()
        return context
