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


class ProductList(Titled, RichText):

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
