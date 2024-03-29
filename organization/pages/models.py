# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from mezzanine.core.models import Displayable, Orderable, TeamOwnable, RichText
from mezzanine.core.fields import FileField
from mezzanine.pages.models import Page, Link as MezzanineLink
from organization.core.models import SubTitled, Block, Image, Link, RelatedTitle,\
    DynamicContent, URL
from organization.media.models import PlaylistRelated
from organization.core.managers import CustomSearchableManager


class CustomPage(Page, SubTitled, RichText):

    objects = CustomSearchableManager()
    menu_alinea = models.BooleanField(_('menu alinea'), default=False)
    class_css = models.CharField(_('CSS class'), max_length=32, blank=True, null=True)

    # order of blocks
    block_order = models.CharField(_(
        '''
        order of blocks (
            0: images,
            1: multimedias,
            2: liste de personnes,
            3: blocks,
            4: listes des produits,
            5: Dynamic Content pages
        )
        '''
        ),
        max_length=32,
        default='0,1,2,3,4,5'
    )

    separator = models.CharField(_(
        '''
        separator before blocks,
        0 : no sepeartor
        1 : separator

        order of blocks (
            0: images,
            1: multimedias,
            2: liste de personnes,
            3: blocks,
            4: listes des produits,
            5: Dynamic Content pages
        )

        '''
        ),
        max_length=32,
        default='0,0,1,1,1,1'
    )

    display_content = models.BooleanField(_('display content'), default=True)

    display_navbar = models.BooleanField(default=True)
    displayed_in_navbars = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'custom page'
        permissions = TeamOwnable.Meta.permissions


class ExtendedCustomPage(Page, SubTitled, RichText):

    objects = CustomSearchableManager()

    class Meta:
        verbose_name = "extended custom page"


class ExtendedCustomPageDynamicContent(models.Model):

    NONE = "none"
    LIST_NEWS = "news"
    LIST_EVENTS = "events"
    LIST_JURY = "jury"

    EXTRA_CONTENT_CHOICES = (
        (NONE, "No extra content"),
        (LIST_NEWS, "List of News"),
        (LIST_EVENTS, "List of Events"),
        (LIST_JURY, "List of the Jury"),
    )

    TEMPLATE_CHOICES = (
        (NONE, ""),
        (LIST_NEWS, "magazine/article/ecp_inc/article_list.html"),
        (LIST_EVENTS, "agenda/ecp_inc/event_list.html"),
        (LIST_JURY, "network/ecp_inc/jury_list.html"),
    )

    page = models.ForeignKey(
        ExtendedCustomPage,
        verbose_name="extended custom page",
        related_name="extra_content",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    extra_content = models.CharField(
        max_length=32,
        choices=EXTRA_CONTENT_CHOICES,
        default=NONE
    )

    @property
    def choice(self):
        return self.extra_content

    @property
    def name(self):
        return self.get_extra_content_display()

    @property
    def template(self):
        try:
            temp = dict(self.TEMPLATE_CHOICES)[self.extra_content]
        except KeyError:
            temp = ""
        return temp


class PageBlock(Block):

    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("block")
        verbose_name_plural = _("blocks")
        verbose_name = 'page block'
        ordering = ['_order', ]


class PageImage(Image):

    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "page"


class PagePlaylist(PlaylistRelated):

    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
        related_name='playlists',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("playlist")
        verbose_name_plural = _("playlists")
        order_with_respect_to = "page"


class PageLink(Link):

    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")
        order_with_respect_to = "page"


DYNAMIC_CONTENT_DISPLAY_MODES = (
    ('0', "Affichage toute largueur"),
    ('1', "Affichage pour menu gauche"),
)


class PageRelatedTitle(RelatedTitle):

    page = models.OneToOneField(
        Page,
        verbose_name=_('page'),
        related_name='related_title',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    display_mode = models.CharField(
        max_length=1,
        choices=DYNAMIC_CONTENT_DISPLAY_MODES,
        default='0'
    )
    as_page_title = models.BooleanField(
        _('Afficher le titre comme un titre de page'),
        default=False
    )
    in_navbar = models.BooleanField(_('in navbar ?'), default=False)

    class Meta:
        verbose_name = _("related title")
        order_with_respect_to = "page"


class DynamicContentPage(DynamicContent, Orderable):

    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
        related_name='dynamic_content_pages',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Dynamic Content Page'


class DynamicMultimediaPage(DynamicContent, Orderable):

    page = models.ForeignKey(
        Page,
        verbose_name=_('page'),
        related_name='dynamic_multimedia',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Multimedia'


class LinkImage(models.Model):

    link = models.ForeignKey(
        MezzanineLink,
        verbose_name=_('link'),
        related_name='link_images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    image = FileField(
        _("Image"),
        max_length=1024,
        format="Image",
        upload_to="images"
    )

    class Meta:
        verbose_name = _("link image")
        verbose_name_plural = _("link images")
        order_with_respect_to = "link"


class LinkStyle(models.Model):

    link = models.OneToOneField(
        MezzanineLink,
        verbose_name=_('link'),
        related_name='link_style',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    class_css = models.CharField(_('CSS class'), max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = _("css class")


class DynamicContentHomeSlider(DynamicContent, Orderable):

    home = models.ForeignKey(
        "home",
        verbose_name=_('home'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Slider'


class DynamicContentHomeBody(DynamicContent, Orderable):

    home = models.ForeignKey(
        "home",
        verbose_name=_('home'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Body')


class DynamicContentHomeMedia(DynamicContent, Orderable):

    home = models.ForeignKey(
        "home",
        verbose_name=_('home'),
        related_name='dynamic_content_home_media',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Media'


class HomeImage(Image, URL):

    home = models.ForeignKey(
        "home",
        verbose_name=_('home'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "home"


class Home(Displayable):

    class Meta:
        verbose_name = _('home')
        verbose_name_plural = _("homes")

    def get_absolute_url(self):
        return reverse("organization-home")
