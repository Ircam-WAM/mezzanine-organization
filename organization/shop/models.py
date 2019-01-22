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

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import RichText, Displayable, Slugged, Orderable
from cartridge.shop.models import Product

from organization.core.models import *


PRODUCT_LIST_STYLE_CHOICES = [
    ('square', _('square')),
    ('circle', _('circle')),
]


class ProductList(Titled, Description, RichText):

    style = models.CharField(_('style'), max_length=16, choices=PRODUCT_LIST_STYLE_CHOICES)

    class Meta:
        verbose_name = _("product list")
        verbose_name_plural = _("product lists")

    def __str__(self):
        return self.title


class ProductListProduct(Orderable):

    list = models.ForeignKey(ProductList, verbose_name=_('product list'), related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='lists', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")


class PageProductList(models.Model):

    page = models.ForeignKey('pages.Page', verbose_name=_('page'), related_name='product_lists', blank=True, null=True, on_delete=models.SET_NULL)
    list = models.ForeignKey('organization-shop.ProductList', verbose_name=_('product list'), related_name='pages', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("product list")
        verbose_name_plural = _("product lists")


class ProductLink(Link):

    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class ProductPrestashopProduct(models.Model):

    product = models.OneToOneField(Product, verbose_name=_('product'), related_name='prestashop_products')
    external_id = models.IntegerField(verbose_name=_('external id'), null=True, blank=True)
    slug = models.CharField(max_length=255, verbose_name=_('slug'), null=True, blank=True)
    url = models.CharField(max_length=512, verbose_name=_('url'), null=True, blank=True)

    class Meta:
        verbose_name = _("prestashop product")
        verbose_name_plural = _("prestashop products")

    def __str__(self):
        return ' - '.join((self.product.title, str(self.external_id)))
