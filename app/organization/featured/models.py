from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings

from organization.core.models import *
from organization.magazine.models import *
from organization.media.models import *

from mezzanine_agenda.models import Event


class Featured(Named):
    """(Featured description)"""

    pages = models.ManyToManyField(BasicPage, verbose_name=_('pages'), related_name='featured', blank=True)
    articles = models.ManyToManyField(Article, verbose_name=_('articles'), related_name='featured', blank=True)
    events = models.ManyToManyField(Event, verbose_name=_('events'), related_name='featured', blank=True)
    videos = models.ManyToManyField(Video, verbose_name=_('videos'), related_name='featured', blank=True)
    playlists = models.ManyToManyField(Playlist, verbose_name=_('playlists'), related_name='featured', blank=True)

    def __unicode__(self):
        return self.name
