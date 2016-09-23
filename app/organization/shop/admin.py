from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import *

from organization.projects.models import *
from organization.pages.models import *
from organization.media.models import Video, Audio
from organization.shop.models import *

from cartridge.shop.admin import *


class ProductBlockProductInline(TabularDynamicInlineAdmin):

    model = ProductBlockProduct


class ProductBlockAdmin(BaseTranslationModelAdmin):

    inlines = [ProductBlockProductInline, ]


class ProductLinkInline(TabularDynamicInlineAdmin):

    model = ProductLink


class CustomProductAdmin(ProductAdmin):

    inlines = [ProductImageAdmin, ProductVariationAdmin, ProductLinkInline]


admin.site.register(ProductBlock, ProductBlockAdmin)
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
