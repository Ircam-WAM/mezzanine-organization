from __future__ import unicode_literals
from future.builtins import str

from django.utils.translation import ugettext_lazy as _

from mezzanine_agenda.models import Event
from organization.core.models import *


class EventBlock(Block):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("block")
        verbose_name_plural = _("blocks")


class EventImage(Image):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
