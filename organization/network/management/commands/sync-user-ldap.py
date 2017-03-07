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

import os
import sys
import csv
import logging
import datetime
import math
import datetimerange
from optparse import make_option
import xlrd
from itertools import takewhile
from re import findall
import dateutil.parser
import sys,ldap,ldap.async
# from string import split
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.text import slugify
from organization.network.models import Person

class Logger:

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def info(self, prefix, message):
        self.logger.info(' ' + prefix + ' : ' + message)

    def error(self, prefix, message):
        self.logger.error(prefix + ' : ' + message)


def get_instance(model, field, value):
    models = model.objects.filter(field=value)
    if models:
        return models[0]
    else:
        model = model()
        model.field = value
        return model



class Command(BaseCommand):
    help = """Import Person data from IRCAM's legacy XLS management file.
              python manage.py import-ircam-timesheet-xls -s /srv/backup/time_sheet_2015_V3_H2020.xls
    """

    option_list = BaseCommand.option_list + (
          make_option('-d', '--dry-run',
            action='store_true',
            dest='dry-run',
            help='Do NOT write anything'),
          make_option('-f', '--force',
            action='store_true',
            dest='force',
            help='Force overwrite data'),
          make_option('-l', '--log',
            dest='log',
            help='define log file'),
    )

    def handle(self, *args, **kwargs):
        self.logger = Logger(kwargs.get('log'))
        self.pattern = kwargs.get('pattern')
        self.dry_run =  kwargs.get('dry-run')
        self.force = kwargs.get('force')


        s = ldap.async.List(
          ldap.initialize(settings.AUTH_LDAP_SERVER_URI),
        )

        s.startSearch(
          'ou=People,dc=ircam,dc=fr',
          ldap.SCOPE_SUBTREE,
          '(objectClass=*)',
        )

        try:
          partial = s.processResults()
        except ldap.SIZELIMIT_EXCEEDED:
          sys.stderr.write('Warning: Server-side size limit exceeded.\n')
        else:
          if partial:
            sys.stderr.write('Warning: Only partial results received.\n')

        sys.stdout.write(
          '%d results received.\n' % (
            len(s.allResults)
          )
        )
        counter = 0
        for user in s.allResults:
            user = user[1][1]
            if 'sn' in user and 'givenName' in user:
                lastname = user['sn'][0].decode("utf-8")
                firstname = user['givenName'][0].decode("utf-8")
                slug = slugify(firstname+'-'+lastname)
                try :
                    p = Person.objects.get(slug=slug)
                    if 'mail' in user:
                        email = user['mail'][0].decode("utf-8")
                        p.email = email
                        p.save()
                        counter += 1
                        self.logger.info('Person', p.first_name + ' ' + p.last_name + " | email : " + p.email )

                except:
                    pass

        self.logger.info('Count', '****************' + str(counter) + ' persons have been processed. *******************' )
