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
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from mezzanine.pages.models import Page, RichText
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.core.models import Displayable, Slugged, Orderable
from mezzanine.utils.urls import admin_url, slugify, unique_slug
from mezzanine.utils.models import base_concrete_model, get_user_model_name

from django_countries.fields import CountryField


COLOR_CHOICES = (('black', _('black')), ('yellow', _('yellow')), ('red', _('red')), ('white', _('white')),)

ALIGNMENT_CHOICES = (('left', _('left')), ('center', _('center')), ('right', _('right')))

IMAGE_TYPE_CHOICES = (('logo', _('logo')), ('logo_white', _('logo white')), ('logo_black', _('logo black')), ('logo_header', _('logo header')), ('logo_footer', _('logo footer')), ('slider', _('slider')), ('card', _('card')), ('page_slider', _('page - slider')), ('page_featured', _('page - featured')))


class Description(models.Model):
    """Abstract model providing a description field"""

    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True


class NamedOnly(models.Model):
    """Abstract model providing a name field only"""

    name = models.CharField(_('name'), max_length=512, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Named(models.Model):
    """Abstract model providing a name field and a description"""

    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True
        ordering = ['name',]

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.__str__())


class NamedSlugged(models.Model):
    """
    Abstract model that handles auto-generating slugs. Each named slugged
    object is also affiliated with a specific site object.
    """

    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), blank=True)
    slug = models.CharField(_("URL"), max_length=2000, blank=True, null=True,
            help_text=_("Leave blank to have the URL auto-generated from "
                        "the name."))

    class Meta:
        abstract = True
        ordering = ['name',]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        If no slug is provided, generates one before saving.
        """
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(NamedSlugged, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Create a unique slug by passing the result of get_slug() to
        utils.urls.unique_slug, which appends an index if necessary.
        """
        # For custom content types, use the ``Page`` instance for
        # slug lookup.
        concrete_model = base_concrete_model(NamedSlugged, self)
        slug_qs = concrete_model.objects.exclude(id=self.id)
        return unique_slug(slug_qs, "slug", self.get_slug())

    def get_slug(self):
        """
        Allows subclasses to implement their own slug creation logic.
        """
        attr = "name"
        if settings.USE_MODELTRANSLATION:
            from modeltranslation.utils import build_localized_fieldname
            attr = build_localized_fieldname(attr, settings.LANGUAGE_CODE)
        # Get self.name_xx where xx is the default language, if any.
        # Get self.name otherwise.
        return slugify(getattr(self, attr, None) or self.name)

    def admin_link(self):
        return "<a href='%s'>%s</a>" % (self.get_absolute_url(),
                                        ugettext("View on site"))
    admin_link.allow_tags = True
    admin_link.short_description = ""


class Titled(models.Model):
    """Abstract model providing a title field"""

    title = models.CharField(_('title'), max_length=1024)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class SubTitled(models.Model):

    sub_title = models.TextField(_('sub title'), blank=True, max_length=1024)

    class Meta:
        abstract = True


class CustomCategory(Named):
    """Category description)"""

    class Meta:
        verbose_name = _('custom category')

    def __str__(self):
        return self.name


class Block(Titled, RichText, Orderable):

    with_separator = models.BooleanField(default=False)
    background_color = models.CharField(_('background color'), max_length=32, choices=COLOR_CHOICES, blank=True)
    login_required = models.BooleanField(_('login required'), default=False)

    class Meta:
        abstract = True


class Image(Titled, Orderable):

    file = FileField(_("Image"), max_length=1024, format="Image", upload_to="images")
    credits = models.CharField(_('credits'), max_length=256, blank=True, null=True)
    type = models.CharField(_('type'), max_length=64, choices=IMAGE_TYPE_CHOICES)

    class Meta:
        abstract = True

    def __str__(self):
        value = self.description
        if not value:
            value = self.file.name
        if not value:
            value = ""
        return value


class UserImage(Titled, Orderable):

    file = models.FileField(_("Image"), max_length=1024, upload_to="user/images/%Y/%m/%d/")
    credits = models.CharField(_('credits'), max_length=256, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        value = self.description
        if not value:
            value = self.file.name
        if not value:
            value = ""
        return value


class File(Titled, Orderable):

    file = FileField(_("document"), max_length=1024, upload_to="documents")

    class Meta:
        abstract = True

    def __str__(self):
        value = self.description
        if not value:
            value = self.file.name
        if not value:
            value = ""
        return value


class DynamicContent(models.Model):

    # used for autocomplete but hidden in admin
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content type'),
        null=True,
        blank=True,
        editable=False,
    )

    # used for autocomplete but hidden in admin
    object_id = models.PositiveIntegerField(
        verbose_name=_('related object'),
        null=True,
        editable=False,
    )

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class URL(models.Model):

    url = models.URLField(_('URL'), max_length=512, blank=True)

    class Meta:
        abstract = True


class LinkType(models.Model):
    """
    A link type could be ``Facebook`` or ``Twitter`` or ``Website``.
    This is masterdata that should be created by the admins when the site is
    deployed for the first time.
    :ordering: Enter numbers here if you want links to be displayed in a
      special order.
    """

    name = models.CharField(max_length=256, verbose_name=_('name'))
    slug = models.SlugField(max_length=256, verbose_name=_('slug'), help_text=_(
            'Use this field to define a simple identifier that can be used'
            ' to style the different link types (i.e. assign social media'
            ' icons to them)'),
        blank=True,
    )
    ordering = models.PositiveIntegerField(verbose_name=_('ordering'), null=True, blank=True)
    fa_option = models.CharField(max_length=64, verbose_name=_('fontawesome icon name option'), null=True, blank=True, help_text="will be added to fa-<slug>")

    class Meta:
        ordering = ['ordering', ]

    def __str__(self):
        return self.name


class Link(URL):
    """A person can have many links."""

    title = models.CharField(_('title'), max_length=1024, null=True, blank=True)
    link_type = models.ForeignKey(LinkType, verbose_name=_('link type'))

    class Meta:
        abstract = True
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return self.url


class Period(models.Model):

    date_from = models.DateField(_('start date'), null=True, blank=True)
    date_to = models.DateField(_('end date'), null=True, blank=True)

    class Meta:
        abstract = True


class PeriodDateTime(models.Model):

    date_from = models.DateTimeField(_('begin date'), null=True, blank=True)
    date_to = models.DateTimeField(_('end date'), null=True, blank=True)

    class Meta:
        abstract = True


class AdminThumbRelatedMixin(object):
    """
    Provides a thumbnail method on models for admin classes to
    reference in the ``list_display`` definition.
    """

    admin_thumb_type = None

    def admin_thumb(self):
        thumb = ""
        if self.admin_thumb_type:
            images = self.images.filter(type=self.admin_thumb_type)
            if images:
                thumb = images[0].file
        if not thumb:
            return ""
        from mezzanine.conf import settings
        from mezzanine.core.templatetags.mezzanine_tags import thumbnail
        x, y = settings.ADMIN_THUMB_SIZE.split('x')
        thumb_url = thumbnail(thumb, x, y)
        return "<img src='%s%s'>" % (settings.MEDIA_URL, thumb_url)
    admin_thumb.allow_tags = True
    admin_thumb.short_description = ""


class Dated(models.Model):

    date_created = models.DateTimeField(_('creation date'), auto_now_add=True)
    date_modified = models.DateTimeField(_('last modification date'), auto_now=True)

    class Meta:
        abstract = True


class Address(models.Model):
    """(Address description)"""

    address = models.TextField(_('address'), blank=True)
    postal_code = models.CharField(_('postal code'), max_length=16, null=True, blank=True)
    city = models.CharField(_('city'), max_length=255, null=True, blank=True)
    country = CountryField(_('country'), null=True, blank=True)

    def __str__(self):
        return ' '.join((self.address, self.postal_code))

    class Meta:
        abstract = True


class RelatedTitle(models.Model):

    title = models.CharField(_('title'), max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True
