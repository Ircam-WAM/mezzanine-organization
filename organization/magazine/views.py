from urllib.parse import urlparse
from django.shortcuts import render
from django.utils import timezone
#from django.views.generic import *
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import *
from django.shortcuts import get_object_or_404
from itertools import chain
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine_agenda.models import Event
from mezzanine.utils.views import paginate
from mezzanine.conf import settings
from organization.magazine.models import Article, Topic, Brief
from organization.network.models import DepartmentPage
from organization.pages.models import CustomPage
from organization.core.views import SlugMixin
from django.template.defaultfilters import slugify


class ArticleDetailView(SlugMixin, DetailView):

    model = Article
    template_name='magazine/article/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        article = self.get_object()
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if article.department:
            context['department_weaving_css_class'] = article.department.pages.first().weaving_css_class
            context['department_name'] = article.department.name
        return context


class ArticleListView(SlugMixin, ListView):

    model = Article
    template_name='magazine/article/article_list.html'
    context_object_name = 'article'

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
        # paginate "manually" articles because we are not in a ListView
        articles = paginate(self.object.articles.all(), self.request.GET.get("page", 1),
                          settings.ARTICLE_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
        context['articles'] = articles
        return context


class ObjectAutocomplete(Select2QuerySetSequenceView):
    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events )

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs


class DynamicContentArticleView(Select2QuerySetSequenceView):
    def get_queryset(self):

        articles = Article.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, events )

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
