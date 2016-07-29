from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from organization.magazine.models import Topic
from organization.core.views import SlugMixin

class HomeView(SlugMixin, TemplateView):

    template_name = 'index.html'
    topics = Topic.objects.all()
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['topics'] = self.topics
        return context
