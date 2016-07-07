from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, OrderField, FileField
from django.conf import settings


ALIGNMENT_CHOICES = (('left', _('left')), ('right', _('right')))
MEDIA_BASE_URL = getattr(settings, 'MEDIA_BASE_URL', 'http://medias.ircam.fr/embed/media/')

# class SubTitle(models.Model):
#
#     sub_title = models.TextField(_('sub title'), blank=True, max_length=1000)
#     class Meta:
#         abstract = True


class BasicPage(Page, RichText):

    sub_title = models.CharField(_('sub title'), blank=True, max_length=1000)
    # description = models.TextField(_('description'), blank=True)
    photo = FileField(_('photo'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_credits = models.CharField(_('photo credits'), max_length=255, blank=True, null=True)
    photo_alignment = models.CharField(_('photo alignment'), choices=ALIGNMENT_CHOICES, max_length=32, default="left", blank=True)
    photo_description = models.TextField(_('photo description'), blank=True)
    photo_featured = FileField(_('photo featured'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_featured_credits = models.CharField(_('photo featured credits'), max_length=255, blank=True, null=True)
