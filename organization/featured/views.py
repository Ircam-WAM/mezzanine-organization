from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from organization.core.views import SlugMixin

class HomeView(SlugMixin, TemplateView):

    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
