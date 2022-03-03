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

import time

from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = "wait for default DB connection"

    db_name = 'default'
    N = 20

    def handle(self, *args, **options):
        i = 0
        connected = False
        db_conn = connections[self.db_name]
        while not connected:
            try:
                db_conn.cursor()
                connected = True
            except Exception:
                print('error connecting to DB...')
                if i > self.N:
                    print('...exiting')
                    raise
                print('...retrying')
                i += 1
                time.sleep(1)
