from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable
from mezzanine.core.fields import RichTextField, OrderField, FileField

from mezzanine_agenda.models import Event

# import eve.models

from .related import SpanningForeignKey

app_label = 'festival'


class MetaCore:

    app_label = 'festival'


class MetaEvent(models.Model):
    """Extensible event metadata"""

    event = models.ForeignKey(Event, related_name='meta_events', verbose_name=_('meta event'), blank=True, null=True, on_delete=models.SET_NULL)
    #eve_event = SpanningForeignKey(eve.models.EventVersion, related_name='festival_events', verbose_name=_('E-venement event'), blank=True, null=True, default=None)
    eve_event_id = models.IntegerField(_('eve id'), blank=True)
    artists = models.ManyToManyField('Artist', related_name='metaevents', verbose_name=_('artists'), blank=True)
    featured = models.BooleanField(_('featured'))
    featured_image = FileField(_('featured image'), upload_to='images/%Y/%m/%d', max_length=1024, blank=True, format="Image")

    class Meta(MetaCore):
        verbose_name = _('meta event')
        db_table = app_label + '_meta_events'

    def __unicode__(self):
        return self.event.title


class Artist(models.Model):
    """Artist"""

    name = models.CharField(_('name'), max_length=255)
    photo = models.ImageField(_('photo'), upload_to='images/%Y/%m/%d', max_length=1024)
    photo_credits = models.CharField(_('photo credits'), max_length=255, blank=True, null=True)
    bio = RichTextField(_("bio"), blank=True, null=True)

    search_fields = ("name", "bio")

    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        verbose_name = _('artist')
        db_table = app_label + '_artists'


class Video(Displayable):
    """Video"""

    event = models.ForeignKey(Event, related_name='videos', verbose_name=_('meta event'), blank=True, null=True, on_delete=models.SET_NULL)
    media_id = models.IntegerField(_('media id'))

    def __unicode__(self):
        return u"Video"
