from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from organization.core.views import SlugMixin
from organization.magazine.models import Brief

class HomeView(SlugMixin, TemplateView):

    template_name = 'index.html'
    briefs = Brief.objects.all() # with .published, order by isn't working anymore

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['briefs'] = self.briefs
        return context

    def get_queryset(self, **kwargs):
        return self.model.objects.published()
