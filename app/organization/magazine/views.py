from urllib.parse import urlparse
from django.shortcuts import render
from django.utils import timezone
#from django.views.generic import *
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import *
from django.shortcuts import get_object_or_404

from organization.magazine.models import Article, Topic, Brief
from organization.team.models import Department

from organization.core.views import SlugMixin
from django.template.defaultfilters import slugify


class ArticleDetailView(SlugMixin, DetailView):

    model = Article
    template_name='magazine/article/article_detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        previous_page_url = request.META['HTTP_REFERER']
        previous_page_slug = request.META['HTTP_REFERER'].rsplit("/")[-2]
        if previous_page_slug:
            #find parents page
            parsed_url = urlparse(previous_page_url)
            self.department_parent = Department.objects.filter(slug=parsed_url.path[1:][:-1])
            self.topic_parent = Topic.objects.filter(slug=previous_page_slug)
        return super(ArticleDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if self.topic_parent:
            context['topic_parent'] = self.topic_parent.all()[0]
        if self.department_parent:
            context['department_parent'] =  self.department_parent.all()[0]
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
