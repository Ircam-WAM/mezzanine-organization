from django.conf import settings # import the settings file
from datetime import datetime, date
from organization.pages.models import Page
from organization.network.models import Organization

def settings(request):
    date_now = datetime.now()
    # SEASON
    current_season = int(date_now.year) - 1 if datetime(date_now.year, 1,1) <= date_now and date_now <= datetime(date_now.year, 7, 31) else date_now.year
    current_season_styled = str(current_season)[-2:]+"."+str(current_season+1)[-2:]

    # NEWSLETTER
    newsletter_page = Page.objects.filter(slug="newsletter")
    newsletter_subscribing_url = ""
    if newsletter_page:
        newsletter_subscribing_url = newsletter_page.first().get_absolute_url()

    # HOST ORGANIZATION
    host_org = Organization.objects.get(is_host=True)
    linked_org_content = host_org.organizations_content.filter(organizations_content__id=host_org.id).order_by('organizations_content__order')
    linked_org_footer = host_org.organizations_footer.filter(organizations_footer__id=host_org.id).order_by('organizations_footer__order')
    research_slug = "recherche"

    return {'current_season': current_season,
            'current_season_styled': current_season_styled,
            'newsletter_subscribing_url': newsletter_subscribing_url,
            'host_organization': host_org,
            'linked_organization_content' : linked_org_content,
            'linked_organization_footer' : linked_org_footer,
            'research_slug' : research_slug
            }
