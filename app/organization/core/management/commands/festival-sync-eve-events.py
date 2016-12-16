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

from datetime import datetime, timedelta
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

import mezzanine_agenda.models as ma_models
from mezzanine.generic.models import AssignedKeyword, Keyword

import eve.models as eve_models


class Command(BaseCommand):
    """Synchronize events from E-vement to mezzanine_agenda"""


    option_list = BaseCommand.option_list + (
          make_option('-m', '--meta_event',
            dest='meta_event',
            help='define eve meta_event'),
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
        meta_event_name = kwargs.get('meta_event')
        meta_trans_all = eve_models.MetaEventTranslation.objects.all()
        for meta_trans in meta_trans_all:
            if meta_trans.name == meta_event_name:
                break
        eve_events = eve_models.Event.objects.filter(meta_event=meta_trans.id)
        for eve_event in eve_events:
            event_trans = eve_models.EventTranslation.objects.filter(id=eve_event, lang='fr')[0]
            manifestations = eve_event.manifestations.all().order_by('happens_at')
            first = True
            for manifestation in manifestations:
                events = ma_models.Event.objects.filter(external_id=manifestation.id)
                if not events:
                    event = ma_models.Event(external_id=manifestation.id)
                else:
                    event = events[0]
                event.start = manifestation.happens_at
                event.end = manifestation.happens_at + timedelta(seconds=manifestation.duration)
                event.title = event_trans.name
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
                event.save()
                keyword, _ = Keyword.objects.get_or_create(title=eve_event.event_category.name)
                event.keywords.add(AssignedKeyword(keyword=keyword), bulk=False)

                eve_prices = eve_models.PriceManifestation.objects.filter(manifestation=manifestation)
                for price in eve_prices:
                    event_price, c = ma_models.EventPrice.objects.get_or_create(value=float(price.value))
                    if event:
                        if not event_price in event.prices.all():
                            event.prices.add(event_price)

                if not first:
                    event.parent = parent
                else:
                    parent = event
                    first = False

                event.save()
