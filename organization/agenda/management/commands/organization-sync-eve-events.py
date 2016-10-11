from datetime import datetime, timedelta
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

import mezzanine_agenda.models as ma_models
from mezzanine.generic.models import AssignedKeyword, Keyword

import eve.models as eve_models
import organization.agenda

class Command(BaseCommand):
    """Synchronize events from E-vement to mezzanine_agenda"""


    option_list = BaseCommand.option_list + (
          make_option('-m', '--meta_event',
            dest='meta_event',
            help='define eve meta_event'),
          )

    default_user = User.objects.get(username='admin')

    def cleanup(self):
        for event in ma_models.Event.objects.all():
            event.delete()
        for location in ma_models.EventLocation.objects.all():
            location.delete()
        for event_price in ma_models.EventPrice.objects.all():
            event_price.delete()
        for period in organization.agenda.models.EventPeriod.objects.all():
            period.delete()

    def handle(self, *args, **kwargs):
        self.cleanup()

        meta_event_name = kwargs.get('meta_event')
        meta_trans_all = eve_models.MetaEventTranslation.objects.all()
        for meta_trans in meta_trans_all:
            if meta_trans.name == meta_event_name:
                break

        eve_events = eve_models.Event.objects.filter(meta_event=meta_trans.id)

        for eve_event in eve_events:
            first = True
            eve_locations = []
            event_trans = eve_models.EventTranslation.objects.filter(id=eve_event, lang='fr')[0]
            event_trans_en = eve_models.EventTranslation.objects.filter(id=eve_event, lang='en')[0]
            manifestations = eve_event.manifestations.all().order_by('happens_at')
            events = ma_models.Event.objects.filter(external_id=eve_event.id)

            if not events:
                event = ma_models.Event(external_id=eve_event.id)
            else:
                event = events[0]

            for manifestation in manifestations:
                if first:
                    event.title = event_trans.name
                    event.title_en = event_trans_en.name
                    event.user = self.default_user
                    locations = ma_models.EventLocation.objects.filter(title=manifestation.location.name)
                    if locations:
                        location = locations[0]
                    else:
                        location = ma_models.EventLocation(title=manifestation.location.name)
                    address = '\n'.join([manifestation.location.address, manifestation.location.postalcode + ' ' + manifestation.location.city])
                    location.address = address
                    location.external_id = manifestation.id
                    location.clean()
                    location.save()
                    event.location = location
                    event.start = manifestation.happens_at
                    event.save()
                    first = False

                period = organization.agenda.models.EventPeriod(event=event)
                period.date_from = manifestation.happens_at
                period.date_to = manifestation.happens_at + timedelta(seconds=manifestation.duration)
                period.save()

                # keyword, c = Keyword.objects.get_or_create(title=eve_event.event_category.name)
                # event.keywords.add(AssignedKeyword(keyword=keyword), bulk=False)

                eve_prices = eve_models.PriceManifestation.objects.filter(manifestation=manifestation)
                for price in eve_prices:
                    event_price, c = ma_models.EventPrice.objects.get_or_create(value=float(price.value))
                    if event:
                        if not event_price in event.prices.all():
                            event.prices.add(event_price)

            event.end = period.date_to
            event.status = 1
            event.save()
