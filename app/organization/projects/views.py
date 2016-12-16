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
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine_agenda.models import Event
from mezzanine.conf import settings
from organization.projects.models import *
from organization.core.views import *
from organization.magazine.views import Article
from organization.pages.models import CustomPage

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
            context['page'] = project.topic.pages.all().first()
        return context


class DynamicContentProjectView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events,)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class ProjectDemoDetailView(SlugMixin, DetailView):

    model = ProjectDemo
    template_name='projects/project_demo_detail.html'
    context_object_name = 'demo'

    def get_context_data(self, **kwargs):
        context = super(ProjectDemoDetailView, self).get_context_data(**kwargs)
        demo = self.get_object()
        project = demo.project
        department = None

        if project:
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
                context['page'] = project.topic.pages.all().first()

        return context
