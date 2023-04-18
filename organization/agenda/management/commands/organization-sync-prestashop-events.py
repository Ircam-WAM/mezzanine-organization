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

from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import mezzanine_agenda.models as ma_models
import organization.agenda.models as oa_models
import prestashop.models as pa_models


class Command(BaseCommand):
    """Synchronize events from PrestaShop to mezzanine_agenda"""

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
        for event in ma_models.Event.objects.all():
            event.delete()

    def handle(self, *args, **kwargs):
        # !! NOT FOR PROD !!
        # self.cleanup()

        products = []
        category_lang_name = kwargs.get('category_lang_name')

        if not category_lang_name:
            for category in pa_models.PsCategoryLang.objects.all():
                print(category.name)

        category_lang_name = kwargs.get('category_lang_name')
        category_lang = pa_models.PsCategoryLang.objects.get(name=category_lang_name)
        category = pa_models.PsCategory.objects.get(
            id_category=category_lang.id_category
        )
        category_products = pa_models.PsCategoryProduct.objects.filter(
            id_category=category.id_category
        )

        for category_product in category_products:
            products.append(
                pa_models.PsProduct.objects.get(
                    id_product=category_product.id_product
                )
            )

        for product in products:
            print('---------------------------')
            print(product.id_product)

            events = ma_models.Event.objects.filter(external_id=product.id_product)
            if events:
                event = events[0]
            else:
                event = ma_models.Event(external_id=product.id_product)

            product_langs = pa_models.PsProductLang.objects.filter(
                id_product=product.id_product
            )
            for product_lang in product_langs:
                lang_code = self.languages[product_lang.id_lang]['code']

                for lang in self.languages:
                    if product_lang.teaching_lang.lower() in self.languages[
                        product_lang.id_lang
                    ]['names']:
                        language = self.languages[product_lang.id_lang]['code']
                        event_training = oa_models.EventTraining(language=language)
                        break

                print(product_lang.name, lang_code, product_lang.dates)

                setattr(event, 'title' + '_' + lang_code, product_lang.name)
                setattr(event, 'content' + '_' + lang_code, product_lang.description)
                event.date_text = product_lang.dates

            event.start = datetime.now()
            event.user = self.default_user
            event_price, c = ma_models.EventPrice.objects.get_or_create(
                value=product.price
            )
            event.save()
            event.prices.add(event_price)
            event.status = 1
            event.save()
            event_training.event = event
            event_training.save()
