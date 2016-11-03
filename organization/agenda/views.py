from django.views.generic.base import TemplateView
from mezzanine.conf import settings

class ConfirmationView(TemplateView):

    template_name = "agenda/confirmation.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmationView, self).get_context_data(**kwargs)
        context['confirmation_url'] = settings.EVENT_CONFIRMATION_URL % kwargs['transaction_id']
        return context
