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
