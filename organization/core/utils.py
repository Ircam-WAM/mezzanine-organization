from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from mezzanine.conf import settings


def split_events_from_other_related_content(context, related_content):
    context["related"] = {}
    context["related"]["other"] = []
    context["related"]["event"] = []
    for rc in related_content:
        if rc.__class__.__name__ == "Event":
            context["related"]["event"].append(rc)
        else :
            context["related"]["other"].append(rc)
    return context        


def get_other_sites():
    #return Site.objects.exclude(pk=settings.SITE_ID)
    return Site.objects.all()

def actions_to_duplicate():
    sites = get_other_sites()
    actions = []
    for site in sites:
        actions.append('duplicate_content_to_' + site.domain.replace(".", "_"))
    return actions
