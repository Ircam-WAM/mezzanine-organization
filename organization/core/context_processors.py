from django.conf import settings # import the settings file
from datetime import datetime, date
from organization.pages.models import Page
from organization.network.models import Organization, OrganizationLinkedInline

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

    # HOST ORGANIZATIONS
    host_org = Organization.objects.get(is_host=True)
    organization_lists = []

    for orga_linked_block in host_org.organization_linked_block.all():
        organizations = []
        for orga_list in OrganizationLinkedInline.objects.filter(organization_list_id=orga_linked_block.organization_linked_id):
            organizations.append(orga_list.organization)
        organization_lists.append(organizations)

    linked_org_content = organization_lists[0] if len(organization_lists) > 0 else None
    linked_org_footer = organization_lists[1] if len(organization_lists) > 1 else None
    linked_org_footer_2 = organization_lists[2] if len(organization_lists) > 2 else None

    research_slug = "recherche"

    return {'current_season': current_season,
            'current_season_styled': current_season_styled,
            'newsletter_subscribing_url': newsletter_subscribing_url,
            'host_organization': host_org,
            'linked_organization_content' : linked_org_content,
            'linked_organization_footer' : linked_org_footer,
            'linked_organization_footer_2' : linked_org_footer_2,
            'research_slug' : research_slug
            }
