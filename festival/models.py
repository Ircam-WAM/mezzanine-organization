from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable
from mezzanine.core.fields import RichTextField, OrderField

import eve.models

from .related import SpanningForeignKey


class MetaCore:

    app_label = 'festival'


class Event(Displayable):
    """(Event description)"""

    event_id = models.IntegerField()
    # event = SpanningForeignKey(eve.models.EventVersion, related_name='festival_events', verbose_name=_('E-venement event'), blank=True, null=True, default=None)
    rich_description = RichText(_('rich description'))
    artists = models.ManyToManyField('Artist', related_name='events', verbose_name=_('artists'), blank=True)

    class Meta(MetaCore):
        verbose_name = _('event')
        db_table = 'event'

    def __unicode__(self):
        return self.title


class Artist(models.Model):
    """(Artist description)"""

    name = models.CharField(_('name'), max_length=255)
    photo = models.ImageField(_('photo'), upload_to='photos/%Y/%m/%d', max_length=1024)
    photo_credits = models.CharField(_('photo credits'), max_length=255, blank=True, null=True)
    bio = RichTextField(_("bio"), blank=True, null=True)

    search_fields = ("name", "bio")

    def __unicode__(self):
        return self.name


class Video(Displayable):
    """(Video description)"""

    media_id = models.IntegerField(_('media ID'))
    artists = models.ManyToManyField('Artist', related_name='videos', verbose_name=_('artists'), blank=True)

    def __unicode__(self):
        return u"Video"


class Location(models.Model):
    """(Location description)"""

    location_id = models.IntegerField()

    def __unicode__(self):
        return u"Location"
