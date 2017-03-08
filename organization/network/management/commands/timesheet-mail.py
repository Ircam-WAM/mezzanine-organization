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
from calendar import monthrange
import datetimerange
from optparse import make_option
import xlrd
from itertools import takewhile
from re import findall
import dateutil.parser
import sys,ldap,ldap.async
from datetime import date
# from string import split
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.text import slugify
from django.template import Context
from organization.network.models import Person, ProjectActivity
from organization.projects.models import ProjectWorkPackage, PersonActivityTimeSheet

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
        make_option('-r', '--reminder',
            action='store_true',
            dest='reminder',
            default=False,
            help='adapt content of the email'),
    )

    def handle(self, *args, **kwargs):
        self.logger = Logger(kwargs.get('log'))
        self.pattern = kwargs.get('pattern')
        self.dry_run =  kwargs.get('dry-run')
        self.force = kwargs.get('force')
        self.reminder = kwargs.get('reminder')

        current_site = Site.objects.get_current()
        curr_month = date.today().month
        curr_year = date.today().year
        first_day_in_month = date(int(curr_year), int(curr_month), 1)
        last_day_in_month = date(int(curr_year), int(curr_month),  monthrange(int(curr_year), int(curr_month))[1])
        work_packages = ProjectWorkPackage.objects.filter(
            Q(date_from__lte=first_day_in_month) & Q(date_to__gte=first_day_in_month)
            | Q(date_from__gte=first_day_in_month) & Q(date_to__lte=last_day_in_month)
            | Q(date_from__lte=last_day_in_month) & Q(date_to__gte=last_day_in_month)
        ).all()
        person_dict = {}

        # select all persons who are assigned to a current work package
        for wp in work_packages:
            project_activities = ProjectActivity.objects.filter(work_packages=wp)
            for project_activitie in project_activities:
                if not project_activitie.activity.person.slug in person_dict:
                    # check wether they already have validated their timesheets for this month
                    timesheet = PersonActivityTimeSheet.objects.filter(year=curr_year, month=curr_month, project=project_activitie.project)
                    if not len(timesheet) :
                        person_dict[project_activitie.activity.person.slug] = project_activitie.activity.person

        # send mail
        # for person_k, person_v in person_dict.items():
        #     if person_v.email:
        #         pass
        person = Person.objects.get(id=849) # test
        print("reminder", self.reminder)
        send_mail(person.first_name, person.last_name, person.email, first_day_in_month, last_day_in_month, current_site.domain, self.reminder)


def send_mail(first_name, last_name, email, date_from, date_to, domain, is_reminder=False):
    subject = "[WWW] Veuillez saisir vos timesheets"
    if is_reminder:
        subject = "[Rappel] " + subject
    to = (email,)
    from_email = settings.DEFAULT_FROM_EMAIL

    ctx = {
        'first_name': first_name,
        'last_name': last_name,
        'date_from': date_from,
        'date_to': date_to,
        'timesheet_url' : "https://"+ domain + reverse('organization-network-timesheet-create-curr-month-view')
    }

    message = get_template('email/timesheet.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return HttpResponse('email_application_notification')
