from __future__ import unicode_literals
from future.builtins import str

from django.utils.translation import ugettext_lazy as _

from mezzanine_agenda.models import *
from organization.core.models import *
from organization.network.models import *


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
        order_with_respect_to = "event"


class EventDepartment(models.Model):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='departments', blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, verbose_name=_('department'), related_name='events', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")


class EventPerson(models.Model):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='persons', blank=True, null=True, on_delete=models.SET_NULL)
    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='events', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")


class EventLink(Link):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")


class EventAudio(Audio):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='audios', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("audio")
        verbose_name_plural = _("audios")
        order_with_respect_to = "event"


class EventVideo(Video):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='videos', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")
        order_with_respect_to = "event"
