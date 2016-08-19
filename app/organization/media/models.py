from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from mezzanine_agenda.models import Event
from django.conf import settings


MEDIA_BASE_URL = getattr(settings, 'MEDIA_BASE_URL', 'http://medias.ircam.fr/embed/media/')


class Media(Displayable, RichText):
    """Media"""

    media_id = models.CharField(_('media id'), max_length=128)
    open_source_url = models.URLField(_('open source URL'), max_length=1024, blank=True)
    closed_source_url = models.URLField(_('closed source URL'), max_length=1024, blank=True)
    poster_url = models.URLField(_('poster'), max_length=1024, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title

    @property
    def uri(self):
        return MEDIA_BASE_URL + self.media_id

    def get_html(self):
        r = requests.get(self.uri)
        return r.content

    def clean(self):
        super(Media, self).clean()
        self.q = pq(self.get_html())
        sources = self.q('source')
        for source in sources:
            if self.open_source_mime_type in source.attrib['type']:
                self.open_source_url = source.attrib['src']
            elif self.closed_source_mime_type in source.attrib['type']:
                self.closed_source_url = source.attrib['src']
        video = self.q('video')
        if len(video):
            if 'poster' in video[0].attrib.keys():
                self.poster_url = video[0].attrib['poster']


class Audio(Media):
    """Audio"""

    open_source_mime_type = 'audio/ogg'
    closed_source_mime_type = 'audio/mp4'

    class Meta:
        verbose_name = _('audio')

    def get_absolute_url(self):
        return reverse("festival-video-detail", kwargs={"slug": self.slug})


class Video(Media):
    """Video"""

    open_source_mime_type = 'video/webm'
    closed_source_mime_type = 'video/mp4'
    category = models.ForeignKey('VideoCategory', related_name='videos', verbose_name=_('category'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('video')

    @property
    def html(self):
        #TODO: get html content from medias.ircam.fr with request module
        pass

    def get_absolute_url(self):
        return reverse("festival-video-detail", kwargs={"slug": self.slug})


class VideoCategory(Slugged):
    """Video Category"""

    class Meta:
        verbose_name = _('video category')

    def count(self):
        return self.videos.published().count()+1


class Playlist(Slugged):
    """(Playlist description)"""

    audios = models.ManyToManyField('Audio', verbose_name=_('audios'), related_name='playlists', blank=True)
    #description = models.OneToOneField('organization-core.Description', verbose_name=_('description'), related_name='description', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
