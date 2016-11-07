from django.conf import settings # import the settings file
from organization.pages.models import Page

def page_static(request):
    NEWSLETTER_SUBSCRIBING_URL = Page.objects.filter(slug="newsletter").first().get_absolute_url()
    return {'NEWSLETTER_SUBSCRIBING_URL': NEWSLETTER_SUBSCRIBING_URL,}
