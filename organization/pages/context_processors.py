from django.conf import settings # import the settings file
from organization.pages.models import Page

def page_static(request):
    newsletter_page = Page.objects.filter(slug="newsletter")
    NEWSLETTER_SUBSCRIBING_URL = ""
    if newsletter_page:
        NEWSLETTER_SUBSCRIBING_URL = newsletter_page.first().get_absolute_url()
    return {'NEWSLETTER_SUBSCRIBING_URL': NEWSLETTER_SUBSCRIBING_URL,}
