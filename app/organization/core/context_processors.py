from django.conf import settings # import the settings file
from datetime import datetime, date
from organization.pages.models import Page
from organization.network.models import Organization

def settings(request):
    date_now = datetime.now()
    # SEASON
    CURRENT_SEASON = int(date_now.year) - 1 if datetime(date_now.year, 1,1) <= date_now and date_now <= datetime(date_now.year, 7, 31) else date_now.year
    CURRENT_SEASON_STYLED = str(CURRENT_SEASON)[-2:]+"."+str(CURRENT_SEASON+1)[-2:]

    # NEWSLETTER
    newsletter_page = Page.objects.filter(slug="newsletter")
    NEWSLETTER_SUBSCRIBING_URL = ""
    if newsletter_page:
        NEWSLETTER_SUBSCRIBING_URL = newsletter_page.first().get_absolute_url()

    # HOST ORGANIZATION
    host_organization = Organization.objects.get(is_host=True)
    linked_organizations_content = host_organization.organizations_content.all()
    linked_organizations_footer = host_organization.organizations_footer.all()
    return {'CURRENT_SEASON': CURRENT_SEASON,
            'CURRENT_SEASON_STYLED': CURRENT_SEASON_STYLED,
            'NEWSLETTER_SUBSCRIBING_URL': NEWSLETTER_SUBSCRIBING_URL,
            'host_organization': host_organization,
            'LINKED_ORGA_CONTENT' : linked_organizations_content,
            'LINKED_ORGA_FOOTER' : linked_organizations_footer
            }
