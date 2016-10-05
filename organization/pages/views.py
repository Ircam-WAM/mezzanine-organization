from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from organization.pages.models import CustomPage
from organization.core.views import SlugMixin
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import Home
from organization.agenda.models import Event

class HomeView(SlugMixin, ListView):

    model = Home
    template_name = 'index.html'
    briefs = Brief.objects.all() # with .published, order by isn't working anymore
    context_object_name = 'home'

    def get_queryset(self, **kwargs):
        homes = self.model.objects.published()
        if homes:
            return homes.latest("publish_date")
        return None

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['briefs'] = self.briefs
        return context


class DynamicContentHomeSliderView(Select2QuerySetSequenceView):

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs


class DynamicContentHomeBodyView(Select2QuerySetSequenceView):

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        briefs = Brief.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            briefs = briefs.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, briefs, events)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs

class NewsletterView(TemplateView):

    template_name = "pages/newsletter.html"
