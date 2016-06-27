from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Category(BaseNameModel):
    """(Category description)"""

    class Meta:
        verbose_name = _('category')

    def __unicode__(self):
        return self.name


class Topic(BaseNameModel):
    """(Topic description)"""

    class Meta:
        verbose_name = _('topic')

    def __unicode__(self):
        return self.name
