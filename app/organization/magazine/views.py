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
from organization.magazine.models import *
from organization.network.models import DepartmentPage
from organization.pages.models import CustomPage, DynamicContentPage
from organization.core.views import SlugMixin
from django.template.defaultfilters import slugify


class ArticleDetailView(SlugMixin, DetailView):

    model = Article
    template_name='magazine/article/article_detail.html'
    context_object_name = 'article'

    def get_object(self, **kwargs):
        articles = self.model.objects.published(for_user=self.request.user).select_related()
        return get_object_or_404(articles, slug=kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)

        # automatic relation : dynamic content page
        pages = DynamicContentPage.objects.filter(object_id=self.object.id).all()
        pages = [p.content_object for p in pages]

        # automatic relation : dynamic content article
        articles = DynamicContentArticle.objects.filter(object_id=self.object.id).all()
        articles = [a.content_object for a in articles]

        # manual relation : get dynamic contents of current article
        dynamic_content = [dca.content_object for dca in self.object.dynamic_content_articles.all()]

        # gather all and order by creation date
        related_content = pages
        related_content = articles
        related_content += dynamic_content
        related_content.sort(key=lambda x: x.created, reverse=True)
        context['related_content'] = related_content

        if self.object.department:
            context['department_weaving_css_class'] = self.object.department.pages.first().weaving_css_class
            context['department_name'] = self.object.department.name
        return context


class ArticleListView(SlugMixin, ListView):

    model = Article
    template_name='magazine/article/article_list.html'
    context_object_name = 'article'

    def get_queryset(self, **kwargs):
        return self.model.objects.published(for_user=self.request.user).select_related()

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
        pages = CustomPage.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            pages = pages.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, events, pages)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
