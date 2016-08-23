from django.shortcuts import render

from organization.projects.models import *
from organization.core.views import *


class ProjectListView(ListView):

    model = Project
    template_name='project/project_list.html'


class ProjectDetailView(SlugMixin, DetailView):

    model = Project
    template_name='project/project_detail.html'
    context_object_name = 'project'
