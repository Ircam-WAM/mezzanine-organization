from django.shortcuts import render
from django.utils import timezone
#from django.views.generic import *
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import *
from django.shortcuts import get_object_or_404

from organization.magazine.models import Article, Topic ,Brief
from organization.core.views import SlugMixin
from django.template.defaultfilters import slugify


class ArticleDetailView(SlugMixin, DetailView):

    model = Article
    template_name='magazine/article/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        return context


class ArticleListView(SlugMixin, ListView):

    model = Article
    template_name='magazine/article/article_list.html'
    # context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        return context


class BriefDetailView(SlugMixin, DetailView):

    model = Brief
    template_name='magazine/inc_brief.html'
    context_object_name = 'brief'

    def get_context_data(self, **kwargs):
        context = super(BriefDetailView, self).get_context_data(**kwargs)
        return context

class BriefListView(SlugMixin, ListView):

    model = Brief
    template_name='magazine/brief/brief_list.html'
    context_object_name = 'brief'

    def get_context_data(self, **kwargs):
        context = super(BriefListView, self).get_context_data(**kwargs)
        return context


class TopicDetailView(SlugMixin, DetailView):

    model = Topic
    template_name='magazine/topic/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        return context
