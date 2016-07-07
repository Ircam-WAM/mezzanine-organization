from django.shortcuts import render
from django.views.generic import *
from django.views.generic.base import *
from django.shortcuts import get_object_or_404

# Create your views here.
class BriefDetailView(SlugMixin, DetailView):

    model = Brief
    template_name='magazine/inc_brief.html'
    context_object_name = 'brief'

    def get_context_data(self, **kwargs):
        context = super(BriefDetailView, self).get_context_data(**kwargs)
        return context
