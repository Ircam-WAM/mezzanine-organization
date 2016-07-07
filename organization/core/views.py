from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic.base import View
from django.views.generic import DetailView, ListView, TemplateView


class SlugMixin(object):

    def get_object(self):
        objects = self.model.objects.all()
        return get_object_or_404(objects, slug=self.kwargs['slug'])


class HomeView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
