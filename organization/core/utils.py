from django.apps import apps
from django.contrib.sites.models import Site


def split_events_from_other_related_content(context, related_content):
    context["related"] = {}
    context["related"]["other"] = []
    context["related"]["event"] = []
    for rc in related_content:
        if rc.__class__.__name__ == "Event":
            context["related"]["event"].append(rc)
        else:
            context["related"]["other"].append(rc)
    return context


def get_other_sites():
    # return Site.objects.exclude(pk=settings.SITE_ID)
    return Site.objects.all()


def actions_to_duplicate():
    sites = get_other_sites()
    actions = []
    for site in sites:
        actions.append('duplicate_content_to_' + site.domain.replace(".", "_"))
    return actions


def getUsersListOfSameTeams(user):
    try:
        try:
            person = user.person
        except Exception:
            from organization.network.models import Person
            person = Person.objects.get(user__id=user.id)
        teams = {x.teams.all() for x in person.activities.all()}
        person_list = []
        person_model = apps.get_model('organization_network.Person')
        for team in teams:
            person_list.extend(
                person_model.objects.filter(activities__teams__in=team).all().distinct()
            )
        user_list = []
        for person in person_list:
            if hasattr(person, 'user') and person.user:
                user_list.append(person.user.id)
        return user_list
    except Exception:
        return []


def usersTeamsIntersection(userA, userB):
    teamsUserA = set()
    if hasattr(userA, 'person'):
        for activities in userA.person.activities.all():
            teamsUserA.update(activities.teams.all())
    teamsUserB = set()
    if hasattr(userB, 'person'):
        for activities in userB.person.activities.all():
            teamsUserB.update(activities.teams.all())
    return teamsUserA & teamsUserB
