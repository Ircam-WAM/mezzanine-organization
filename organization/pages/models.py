from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from mezzanine.core.models import Displayable, Slugged, Orderable
from mezzanine.pages.models import Link as MezzanineLink
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


class PagePlaylist(PlaylistRelated):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("playlist")
        verbose_name_plural = _("playlists")
        order_with_respect_to = "page"


class PageLink(Link):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        order_with_respect_to = "page"


class DynamicContentPage(DynamicContent, Orderable):

    page = models.ForeignKey(Page, verbose_name=_('page'), related_name='dynamic_content_pages', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Page'


class LinkImage(models.Model):

    link = models.ForeignKey(MezzanineLink, verbose_name=_('link'), related_name='link_images', blank=True, null=True, on_delete=models.SET_NULL)
    image = FileField(_("Image"), max_length=1024, format="Image", upload_to="images")

    class Meta:
        verbose_name = _("link image")
        verbose_name_plural = _("link images")
        order_with_respect_to = "link"


class DynamicContentHomeSlider(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Slider'


class DynamicContentHomeBody(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Body')


class DynamicContentHomeMedia(DynamicContent, Orderable):

    home = models.ForeignKey("home", verbose_name=_('home'), related_name='dynamic_content_home_media', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Media'


class Home(Displayable):

    class Meta:
        verbose_name = _('home')
        verbose_name_plural = _("homes")

    def get_absolute_url(self):
        return reverse("organization-home")

        verbose_name = _('Person List')
