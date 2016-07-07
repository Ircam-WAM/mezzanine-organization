from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged

from organization.structure.models import Person, Organization


class Project(Displayable, RichText):
    """(Project description)"""

    persons = models.ManyToManyField(Person, verbose_name=_('persons'))
    partners = models.ManyToManyField(Organization, verbose_name=_('organizations'))

    def __unicode__(self):
        return self.title
