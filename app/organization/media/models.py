from __future__ import unicode_literals

from pyquery import PyQuery as pq

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.managers import SearchableManager
from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from organization.core.models import *
from mezzanine_agenda.models import Event
from django.conf import settings
import requests


MEDIA_BASE_URL = getattr(settings, 'MEDIA_BASE_URL', 'http://medias.ircam.fr/embed/media/')

PLAYLIST_TYPE_CHOICES = [
    ('audio', _('audio')),
    ('video', _('video')),
]

class Media(Displayable):
    """Media"""

    external_id = models.CharField(_('media id'), max_length=128)
    poster_url = models.URLField(_('poster'), max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('MediaCategory', verbose_name=_('category'), related_name='medias', blank=True, null=True, on_delete=models.SET_NULL)

    # objects = SearchableManager()
    search_fields = ("title",)

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "medias"
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-media-detail", kwargs={"slug": self.slug})

    @property
    def uri(self):
        return MEDIA_BASE_URL + self.external_id

    def get_html(self):
        r = requests.get(self.uri)
        return r.content


def create_media(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.
    if not created or raw:
        return

    q = pq(instance.get_html())
    sources = q('source')

    video = q('video')
    if len(video):
        if 'poster' in video[0].attrib.keys():
            instance.poster_url = video[0].attrib['poster']

    for source in sources:
        mime_type = source.attrib['type']
        transcoded = MediaTranscoded(media=instance, mime_type=mime_type)
        transcoded.url = source.attrib['src']
        transcoded.save()

    instance.save()

models.signals.post_save.connect(create_media, sender=Media, dispatch_uid='create_media')


class MediaTranscoded(models.Model):

    media = models.ForeignKey('Media', verbose_name=_('media'), related_name='transcoded')
    file = FileField(_("file"), max_length=1024, upload_to="uploads/media/")
    url = models.URLField(_('URL'), max_length=1024, blank=True)
    mime_type = models.CharField(_('mime type'), max_length=64)

    preferred_mime_type = ['video/webm', 'audio/ogg']

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "medias"

    def __str__(self):
        return self.url


class MediaCategory(Slugged, Description):
    """Media Category"""

    class Meta:
        verbose_name = _('media category')
        verbose_name_plural = _('media categories')

    def count(self):
        return self.medias.published().count()+1


class Playlist(Displayable):
    """Playlist"""

    type = models.CharField(_('type'), max_length=32, choices=PLAYLIST_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = _('playlist')
        verbose_name_plural = _('playlists')

    def get_absolute_url(self):
        return reverse("organization-playlist-detail", kwargs={"slug": self.slug})


class PlaylistMedia(models.Model):
    """Playlist media"""

    playlist = models.ForeignKey(Playlist, verbose_name=_('playlist'), related_name='medias', blank=True, null=True, on_delete=models.SET_NULL)
    media = models.ForeignKey(Media, verbose_name=_('media'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('media')
        verbose_name_plural = _('medias')
