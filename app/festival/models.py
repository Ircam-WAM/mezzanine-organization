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

ALIGNMENT_CHOICES = (('left', _('left')), ('right', _('right')))

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


class Artist(Displayable, RichText, AdminThumbMixin):
    """Artist"""

    bio = RichTextField(_('biography'), blank=True)
    photo = FileField(_('photo'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_credits = models.CharField(_('photo credits'), max_length=255, blank=True, null=True)
    photo_alignment = models.CharField(_('photo alignment'), choices=ALIGNMENT_CHOICES, max_length=32, default="left", blank=True)
    photo_description = models.TextField(_('photo description'), blank=True)
    featured = models.BooleanField(_('featured'), default=False)
    photo_featured = FileField(_('photo featured'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_featured_credits = models.CharField(_('photo featured credits'), max_length=255, blank=True, null=True)
    events = models.ManyToManyField(Event, related_name='artists', verbose_name=_('events'), blank=True)

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
    media_id = models.CharField(_('media id'), max_length=128)

    class Meta(MetaCore):
        verbose_name = _('video')
        db_table = app_label + '_videos'

    def __unicode__(self):
        return self.title

    @property
    def html(self):
        #TODO: get html content from medias.ircam.fr with request module
        pass

    def get_absolute_url(self):
        return reverse("festival-video-detail", kwargs={"slug": self.slug})


class PageCategory(BaseNameModel):
    """Page Category"""

    class Meta(MetaCore):
        verbose_name = _('page category')
