from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *

from organization.core.admin import *
from organization.projects.models import *
from organization.pages.models import *
from organization.media.models import Video, Audio
from organization.shop.models import *

from cartridge.shop.admin import *


class ProductListProductInline(TabularDynamicInlineAdmin):

    model = ProductListProduct


class ProductListAdmin(BaseTranslationOrderedModelAdmin):

    inlines = [ProductListProductInline, ]
    first_fields = ['title', 'description',]


class ProductLinkInline(TabularDynamicInlineAdmin):

    model = ProductLink


class CustomProductAdmin(ProductAdmin):

    inlines = [ProductImageAdmin, ProductVariationAdmin, ProductLinkInline]


admin.site.register(ProductList, ProductListAdmin)
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
