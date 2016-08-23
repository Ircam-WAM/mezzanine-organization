from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings

from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.blog.models import BlogPost
from mezzanine.pages.models import Page

from organization.core.models import *

import requests
from pyquery import PyQuery as pq


class Artist(Displayable, RichText, AdminThumbMixin):
    """Artist"""

    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    bio = RichTextField(_('biography'), blank=True)
    search_fields = ("title", "bio")

    class Meta:
        verbose_name = _('artist')
        ordering = ['last_name',]

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title
