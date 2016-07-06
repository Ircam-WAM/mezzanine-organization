from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from organization.core.models import Named


class Category(Named):
    """(Category description)"""

    class Meta:
        verbose_name = _('category')

    def __unicode__(self):
        return self.name


class Topic(Named):
    """(Topic description)"""

    class Meta:
        verbose_name = _('topic')

    def __unicode__(self):
        return self.name
