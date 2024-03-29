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

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = """Search for duplicates of Person by first_name and last_name
    """

    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            cursor.execute('SELECT "first_name", "last_name", count(*) \
            FROM "organization_network_person" \
            GROUP BY "first_name", "last_name" HAVING count(*) > 1')
            rows = cursor.fetchall()

        for row in rows:
            print(row)
