from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from mezzanine.core.models import Displayable, Slugged, Orderable
from organization.core.models import *
from organization.media.models import *


class CustomPage(Page, SubTitled, RichText):

    class Meta:
        verbose_name = 'custom page'


class PageBlock(Block):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("block")
        verbose_name_plural = _("blocks")
        verbose_name = 'page block'


class PageImage(Image):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "page"


class PageAudio(Audio):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='audios', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("audio")
        verbose_name_plural = _("audios")
        order_with_respect_to = "page"


class PageVideo(Video):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='videos', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")
        order_with_respect_to = "page"


class PageLink(Link):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        order_with_respect_to = "page"


class DynamicContentHomeSlider(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Home Slider'


class DynamicContentHomeBody(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Home Body'


class Home(Displayable):

    class Meta:
        verbose_name = _('home')
        verbose_name_plural = _("homes")

    def get_absolute_url(self):
        return reverse("organization-home")
