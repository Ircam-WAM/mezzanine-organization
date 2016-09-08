from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
# from mezzanine_agenda.models import Event
from organization.pages.models import CustomPage
from organization.core.views import SlugMixin
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import Home, JobOffer, JobResponse
from organization.pages.forms import JobResponseForm

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


class JobOfferDetailView(CreateView):

    model = JobResponse
    template_name='pages/joboffer/job_offer_detail.html'
    context_object_name = 'job_offer'
    form_class = JobResponseForm

    def get_context_data(self, **kwargs):
        context = super(JobOfferDetailView, self).get_context_data(**kwargs)
        job_offer = JobOffer.objects.get(slug=self.kwargs['slug'])
        if job_offer :
            context['job_offer'] = job_offer
        return context

    def get_initial(self):
        initial = super(JobOfferDetailView, self).get_initial()
        job_offer = JobOffer.objects.get(slug=self.kwargs['slug'])
        if job_offer :
            initial['job_offer'] = job_offer
        return initial

    def get_success_url(self):
        return reverse_lazy('organization-job-offer-detail', kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        messages.info(self.request, _("You have successfully submitted your application."))
        return super(JobOfferDetailView, self).form_valid(form)


class JobOfferListView(ListView):

    model = JobOffer
    template_name='pages/joboffer/job_offer_list.html'
    context_object_name = 'job_offer'

    def get_queryset(self, **kwargs):
        return self.model.objects.published()

    def get_context_data(self, **kwargs):
        context = super(JobOfferListView, self).get_context_data(**kwargs)
        return context


# class JobResponseCreate(CreateView):
#
#     template_name = 'pages/joboffer/inc/job_response_form.html'
#     model = JobResponse
#     # form_class = JobResponseForm
#     fields = ['first_name', 'last_name', 'email', 'curriculum_vitae', 'cover_letter']
#     # success_url = '/job-offer-success/'
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         # form.send_email()
#         return super(JobResponseView, self).form_valid(form)


class DynamicContentHomeSliderView(Select2QuerySetSequenceView):
    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        # events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            # events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage ) #, events

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
        # events = Event.objects.all()
        briefs = Brief.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            # events = events.filter(title__icontains=self.q)
            briefs = briefs.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, briefs) #, events

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
