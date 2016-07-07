from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from mezzanine.blog.models import *

from mezzanine_agenda.models import Event

from organization.magazine.models import *
from organization.core.models import *


class Article(BlogPost):

    sub_title = models.CharField(_('sub title'), blank=True, max_length=1000)

    class Meta:
        verbose_name = _('article')


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
