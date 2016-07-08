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

    def get_absolute_url(self):
        return reverse("magazine-article-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('article')

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("article")
        ordering = ("-publish_date",)    


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
