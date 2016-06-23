from __future__ import unicode_literals

from django.db import models

from organization import Person




class Project(Displayable, RichText):
    """(Project description)"""

    persons = models.ManyToManyField('Person', verbose_name=_('persons'))

    def __unicode__(self):
        return title
