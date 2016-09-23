from datetime import datetime, timedelta
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from mezzanine.generic.models import AssignedKeyword, Keyword

import mezzanine_agenda.models as ma_models
import prestashop.models as pa_models


class Command(BaseCommand):
    """Synchronize events from PrestaShop to mezzanine_agenda"""


    option_list = BaseCommand.option_list + (
          make_option('-c', '--category',
            dest='category_lang_name',
            help='define prestashop PsCategoryLang'),
          )

    default_user = User.objects.get(username='admin')

    def cleanup(self):
        # for event in ma_models.Event.objects.all():
        #     event.delete()
        # for location in ma_models.EventLocation.objects.all():
        #     location.delete()
        for event_price in ma_models.EventPrice.objects.all():
            event_price.delete()

    def handle(self, *args, **kwargs):
        # self.cleanup()
        category_lang_name = kwargs.get('category_lang_name')
        category_lang = pa_models.PsCategoryLang.objects.get(name=category_lang_name)
        category = pa_models.PsCategory.objects.get(id_category=category_lang.id_category)
        products = pa_models.PsProduct.objects.filter(id_category_default=category.id_category)

        for product in products:
            product_langs = pa_models.PsProductLang.objects.filter(id_product=product.id_product)
            for product_lang in product_langs:
                print(product_lang.name, product_lang.dates, product_lang.times)

        # meta_trans_all = eve_models.MetaEventTranslation.objects.all()
        # for meta_trans in meta_trans_all:
        #     if meta_trans.name == meta_event_name:
        #         break
        # eve_events = eve_models.Event.objects.filter(meta_event=meta_trans.id)
        # for eve_event in eve_events:
        #     event_trans = eve_models.EventTranslation.objects.filter(id=eve_event, lang='fr')[0]
        #     manifestations = eve_event.manifestations.all().order_by('happens_at')
        #     first = True
        #     for manifestation in manifestations:
        #         events = ma_models.Event.objects.filter(external_id=manifestation.id)
        #         if not events:
        #             event = ma_models.Event(external_id=manifestation.id)
        #         else:
        #             event = events[0]
        #         event.start = manifestation.happens_at
        #         event.end = manifestation.happens_at + timedelta(seconds=manifestation.duration)
        #         event.title = event_trans.name
        #         event.user = self.default_user
        #
        #         locations = ma_models.EventLocation.objects.filter(title=manifestation.location.name)
        #         if locations:
        #             location = locations[0]
        #         else:
        #             location = ma_models.EventLocation(title=manifestation.location.name)
        #         address = '\n'.join([manifestation.location.address, manifestation.location.postalcode + ' ' + manifestation.location.city])
        #         location.address = address
        #         location.external_id = manifestation.id
        #         location.clean()
        #         location.save()
        #         event.location = location
        #         event.save()
        #         keyword, _ = Keyword.objects.get_or_create(title=eve_event.event_category.name)
        #         event.keywords.add(AssignedKeyword(keyword=keyword), bulk=False)
        #
        #         eve_prices = eve_models.PriceManifestation.objects.filter(manifestation=manifestation)
        #         for price in eve_prices:
        #             event_price, c = ma_models.EventPrice.objects.get_or_create(value=float(price.value))
        #             if event:
        #                 if not event_price in event.prices.all():
        #                     event.prices.add(event_price)
        #
        #         if not first:
        #             event.parent = parent
        #         else:
        #             parent = event
        #             first = False
        #
        #         event.save()
