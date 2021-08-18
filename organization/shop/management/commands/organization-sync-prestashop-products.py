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

from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import organization.shop.models as os_models
import prestashop.models as pa_models
import cartridge.shop.models as ca_models


class Command(BaseCommand):
    """Synchronize products from PrestaShop to cartridge.shop

    ex: python manage.py organization-sync-prestashop-products -c "Forumnet"
    """

    option_list = BaseCommand.option_list + (
        make_option(
            '-c',
            '--category',
            dest='category_lang_name',
            help='define prestashop PsCategoryLang'),
        )

    default_user = User.objects.get(username='admin')
    languages = {
        1: {'code': 'en', 'names': ['english', 'anglais']},
        2: {'code': 'fr', 'names': ['french', 'français']},
    }

    def cleanup(self):
        for product in ca_models.ProductVariation.objects.all():
            product.delete()
        for product in ca_models.Product.objects.all():
            product.delete()

    def handle(self, *args, **kwargs):
        # !! NOT FOR PROD !!
        # self.cleanup()

        products = []
        category_lang_name = kwargs.get('category_lang_name')

        if not category_lang_name:
            for category in pa_models.PsCategoryLang.objects.all():
                print(category.name)
            return

        category_lang_name = kwargs.get('category_lang_name')
        category_lang = pa_models.PsCategoryLang.objects.filter(
            name=category_lang_name
        )[0]
        category = pa_models.PsCategory.objects.get(
            id_category=category_lang.id_category
        )
        category_products = pa_models.PsCategoryProduct.objects.filter(
            id_category=category.id_category
        )

        for category_product in category_products:
            try:
                products.append(pa_models.PsProduct.objects.get(
                    id_product=category_product.id_product)
                )
            except Exception:
                continue

        for product in products:
            print('---------------------------')
            print(product.id_product)

            ca_product, c = ca_models.Product.objects.get_or_create(
                sku=product.reference
            )
            variation, c = ca_models.ProductVariation.objects.get_or_create(
                product=ca_product,
                default=True
            )

            product_langs = pa_models.PsProductLang.objects.filter(
                id_product=product.id_product
            )
            for product_lang in product_langs:
                if product_lang.id_lang in self.languages.keys():
                    lang_code = self.languages[product_lang.id_lang]['code']
                    print(product_lang.name, lang_code)
                    setattr(ca_product, 'title' + '_' + lang_code, product_lang.name)
                    setattr(
                        ca_product, 'content' +
                        '_' +
                        lang_code, product_lang.description
                    )
                    if lang_code == 'en':
                        slug = product_lang.link_rewrite

            ca_product.sku = product.reference
            ca_product.sale_price = product.price
            ca_product.status = 1
            ca_product.save()

            prestashop_product, c = os_models.ProductExternalShop.objects.get_or_create(
                product=ca_product,
                external_id=product.id_product
            )
            prestashop_product.slug = slug
            prestashop_product.save()
