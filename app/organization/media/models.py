from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to

ALIGNMENT_CHOICES = (('left', _('left')), ('center', _('center')), ('right', _('right')))


class Photos(models.Model):
    """Photo bundle with credits"""

    photo = FileField(_('photo'), upload_to='images/photos', max_length=1024, blank=True, format="Image")
    photo_credits = models.CharField(_('photo credits'), max_length=255, blank=True, null=True)
    photo_alignment = models.CharField(_('photo alignment'), choices=ALIGNMENT_CHOICES, max_length=32, default="left", blank=True)
    photo_description = models.TextField(_('photo description'), blank=True)

    photo_card = FileField(_('card photo'), upload_to='images/photos/card', max_length=1024, blank=True, format="Image")
    photo_card_credits = models.CharField(_('photo card credits'), max_length=255, blank=True, null=True)

    photo_slider = FileField(_('slider photo'), upload_to='images/photos/slider', max_length=1024, blank=True, format="Image")
    photo_slider_credits = models.CharField(_('photo slider credits'), max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
