from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from mezzanine.core.models import RichText, Displayable
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from mezzanine_agenda.models import Event

# import eve.models

from .related import SpanningForeignKey

app_label = 'festival'


class MetaCore:

    app_label = 'festival'


class BaseNameModel(models.Model):
    """Base object with name and description"""

    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True)

    class Meta(MetaCore):
        abstract = True

    def __unicode__(self):
        return self.name

class BaseTitleModel(models.Model):
    """Base object with title and description"""

    title = models.CharField(_('title'), max_length=512)
    description = models.TextField(_('description'), blank=True)

    class Meta(MetaCore):
        abstract = True

    def __unicode__(self):
        return self.title


class FestivalEvent(models.Model):
    """Extensible event metadata"""

    event = models.ForeignKey(Event, related_name='festival_events', verbose_name=_('festival event'), blank=True, null=True, on_delete=models.SET_NULL)
    #eve_event = SpanningForeignKey(eve.models.EventVersion, related_name='festival_events', verbose_name=_('E-venement event'), blank=True, null=True, default=None)
    eve_event_id = models.IntegerField(_('eve id'), blank=True)
    category = models.ForeignKey('EventCategory', related_name='festival_events', verbose_name=_('category'), blank=True, null=True, on_delete=models.SET_NULL)
    artists = models.ManyToManyField('Artist', related_name='metaevents', verbose_name=_('artists'), blank=True)
    featured = models.BooleanField(_('featured'), default=False)
    featured_image = FileField(_('featured image'), upload_to='images/events', max_length=1024, blank=True, format="Image")
    featured_image_header = FileField(_('featured image header'), upload_to='images/events/headers', max_length=1024, blank=True, format="Image")

    class Meta(MetaCore):
        verbose_name = _('festival event')
        db_table = app_label + '_events'

    def __unicode__(self):
        return self.event.title


class Artist(Displayable, RichText, AdminThumbMixin):
    """Artist"""

    bio = RichTextField(_('biography'), blank=True)
    photo = FileField(_('photo'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_credits = models.CharField(_('photo credits'), max_length=255, blank=True, null=True)
    featured = models.BooleanField(_('featured'), default=False)

    search_fields = ("title", "bio")

    class Meta(MetaCore):
        verbose_name = _('artist')
        db_table = app_label + '_artists'

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        return reverse("festival-artist-detail", kwargs={'slug': self.slug})


class Video(Displayable, RichText):
    """Video"""

    event = models.ForeignKey(Event, related_name='videos', verbose_name=_('event'), blank=True, null=True, on_delete=models.SET_NULL)
    media_id = models.IntegerField(_('media id'))

    class Meta(MetaCore):
        verbose_name = _('video')
        db_table = app_label + '_videos'

    def __unicode__(self):
        return self.title

    @property
    def html(self):
        #TODO: get html content from medias.ircam.fr with request module
        pass

    @models.permalink
    def get_absolute_url(self):
        return reverse("festival-video-detail", kwargs={"slug": self.slug})


class EventCategory(BaseNameModel):
    """Event Category"""

    class Meta(MetaCore):
        verbose_name = _('event category')


class PageCategory(BaseNameModel):
    """Page Category"""

    class Meta(MetaCore):
        verbose_name = _('page category')
