from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged, Orderable

from organization.core.models import *
from organization.pages.models import *


class Project(CustomDisplayable, Period, RichText):
    """(Project description)"""

    lead_team = models.ForeignKey('organization-network.Team', verbose_name=_('lead team'), related_name='leader_projects', blank=True, null=True)
    persons = models.ManyToManyField('organization-network.Person', verbose_name=_('persons'), blank=True)
    teams = models.ManyToManyField('organization-network.Team', verbose_name=_('teams'), related_name='patner_projects', blank=True)
    organizations = models.ManyToManyField('organization-network.Organization', verbose_name=_('organizations'), blank=True)
    website = models.URLField(_('website'), max_length=512, blank=True)

    class Meta:
        verbose_name = _('project')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-project-detail", kwargs={"slug": self.slug})
