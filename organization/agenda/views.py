from django.views.generic.base import TemplateView
from mezzanine.conf import settings
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
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

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events,)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

        return qs
