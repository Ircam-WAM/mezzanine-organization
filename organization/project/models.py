from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged

from organization.team.models import Person, Team, Organization


class Project(Displayable, RichText):
    """(Project description)"""

    leader_team = models.ForeignKey(Team, verbose_name=_('lead team'), related_name='project_leader', blank=True, null=True)
    partner_persons = models.ManyToManyField(Person, verbose_name=_('partner persons'), blank=True)
    partner_teams = models.ManyToManyField(Team, verbose_name=_('partner teams'), related_name='project_partners', blank=True)
    partner_organizations = models.ManyToManyField(Organization, verbose_name=_('partner organizations'), blank=True)

    def __unicode__(self):
        return self.title
