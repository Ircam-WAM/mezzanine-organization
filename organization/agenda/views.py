from django.views.generic.base import TemplateView
from mezzanine.conf import settings
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from organization.network.models import TeamPage
from organization.projects.models import Project
from organization.magazine.models import Article
from organization.pages.models import CustomPage
from mezzanine_agenda.models import Event

class ConfirmationView(TemplateView):

    template_name = "agenda/confirmation.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmationView, self).get_context_data(**kwargs)
        context['confirmation_url'] = settings.EVENT_CONFIRMATION_URL % kwargs['transaction_id']
        return context


class DynamicContentEventView(Select2QuerySetSequenceView):

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        teampages = TeamPage.objects.all()
        projects = Project.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            teampages = teampages.filter(title__icontains=self.q)
            projects = projects.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events, teampages, projects)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
