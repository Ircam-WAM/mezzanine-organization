from __future__ import unicode_literals
from future.builtins import str

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
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


class EventPeriod(PeriodDateTime):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='periods', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("period")
        verbose_name_plural = _("periods")


class EventPublicType(Named):

    class Meta:
        verbose_name = _("public type")
        verbose_name_plural = _("public types")


class EventTrainingLevel(Named):

    class Meta:
        verbose_name = _("training level")
        verbose_name_plural = _("training levels")


class EventTraining(models.Model):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='trainings', blank=True, null=True, on_delete=models.SET_NULL)
    language = models.CharField(_('Language'), max_length=64, blank=True, null=True, choices=settings.LANGUAGES)
    public_type = models.ForeignKey(EventPublicType, verbose_name=_('public type'), related_name='trainings', blank=True, null=True, on_delete=models.SET_NULL)
    level = models.ForeignKey(EventTrainingLevel, verbose_name=_('level'), related_name='trainings', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("training")
        verbose_name_plural = _("trainings")
