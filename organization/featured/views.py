from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from organization.core.views import SlugMixin
from organization.magazine.models import Brief
