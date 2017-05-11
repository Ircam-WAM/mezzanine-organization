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
from collections import OrderedDict
from pprint import pprint
from calendar import monthrange
import datetimerange
from optparse import make_option
import xlrd
from itertools import takewhile
from re import findall
import dateutil.parser
import sys,ldap,ldap.async
from datetime import date, timedelta, datetime
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


checkboxes = {'True' : 'X', 'False' : '-'}

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

    log_file = settings.TIMESHEET_LOG_PATH + datetime.today().strftime("%y-%m-%d_%H-%m-%S") + ".log"

    def add_arguments(self, parser):

        parser.add_argument(
            '--reminder',
            action='store_true',
            dest='reminder',
            default=False,
            help='adapt content of the email',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Do not send emails',
        )


    def handle(self, *args, **kwargs):
        print("self.log_file", self.log_file)
        self.logger = Logger(self.log_file)
        self.dry_run =  kwargs.get('dry_run')
        self.reminder = kwargs.get('reminder')

        current_site = Site.objects.get_current()

        # get previous month
        last_day_in_month = date.today().replace(day=1) - timedelta(days=1)
        first_day_in_month = last_day_in_month.replace(day=1)
        if settings.DEBUG :
            last_day_in_month = datetime.strptime("2017/03/31", "%Y/%m/%d")
            first_day_in_month = datetime.strptime("2017/03/01", "%Y/%m/%d")
        curr_month = first_day_in_month.month
        curr_year = first_day_in_month.year
        person_dict = OrderedDict()

        # select all persons which have been a assigned to a workpackage or project
        person_list = ProjectActivity.objects.filter((Q(project__date_from__lt=first_day_in_month) & Q(project__date_to__range=(first_day_in_month, last_day_in_month))
                                                    | Q(project__date_from__range=(first_day_in_month, last_day_in_month)) & Q(project__date_to__range=(first_day_in_month, last_day_in_month))
                                                    | Q(project__date_from__range=(first_day_in_month, last_day_in_month)) & Q(project__date_to__gt=last_day_in_month)
                                                    | Q(project__date_from__lt=first_day_in_month) & Q(project__date_to__gt=last_day_in_month))
                                                    | (Q(work_packages__date_from__lt=first_day_in_month) & Q(work_packages__date_to__range=(first_day_in_month, last_day_in_month))
                                                    | Q(work_packages__date_from__range=(first_day_in_month, last_day_in_month)) & Q(work_packages__date_to__range=(first_day_in_month, last_day_in_month))
                                                    | Q(work_packages__date_from__range=(first_day_in_month, last_day_in_month)) & Q(work_packages__date_to__range=(first_day_in_month, last_day_in_month))
                                                    | Q(work_packages__date_from__lt=first_day_in_month) & Q(work_packages__date_to__gt=last_day_in_month))) \
        .exclude(Q(project__date_from__isnull=True) and Q(project__date_to__isnull=True)) \
        .values('activity__id', 'activity__person__id', 'activity__person__first_name', 'activity__person__last_name', 'activity__person__email', 'project__title', 'project__id', 'work_packages__title') \
        .order_by('activity__person__id') \
        .distinct() \
        .all()
        for person in person_list:
            pid = person['activity__person__id']
            if pid not in person_dict.keys():
                person_dict[pid] = {}
            person_dict[pid]['firstname'] = person['activity__person__first_name']
            person_dict[pid]['lastname'] = person['activity__person__last_name']
            person_dict[pid]['email'] = person['activity__person__email']
            if not 'project' in person_dict[pid]:
                person_dict[pid]['project'] = {}
            if not person['project__id'] in person_dict[pid]['project'].keys():
                person_dict[pid]['project'][person['project__id']] = {}
            person_dict[pid]['project'][person['project__id']]['name'] = person['project__title']
            if not 'work_packages' in person_dict[pid]['project'][person['project__id']].keys():
                person_dict[pid]['project'][person['project__id']]['work_packages'] = []
            person_dict[pid]['project'][person['project__id']]['work_packages'].append(person['work_packages__title'])
            person_dict[pid]['activity'] = person['activity__id']

        # test send mail
        if settings.DEBUG :
            person = Person.objects.get(id=settings.TIMESHEET_USER_TEST) # test
            send_mail(person.first_name,
                person.last_name,
                person.email,
                first_day_in_month,
                last_day_in_month,
                current_site.domain,
                self.reminder,
                self.log_file)

        l_head = log_head(first_day_in_month, last_day_in_month)
        # sending mail to all if person has not enterred its timesheet and if not DEBUG mode
        for pid, person_v in person_dict.items():
            l_reminder = log_reminder(False)
            l_timesheet = log_timehseet(False)
            l_person = log_person(str(pid), person_v['firstname'], person_v['lastname'], person_v['project'])
            timesheet = []
            for project_id, project_v in person_v['project'].items():
                t = PersonActivityTimeSheet \
                                     .objects \
                                     .filter(activity__id=person_v['activity'], year=curr_year, month=curr_month, project__id=project_id) \
                                     .exclude(percentage__isnull=True)
                timesheet.extend(t)


            # if person has not entered its timesheets
            if len(timesheet) < len(person_v['project']) :
                if self.reminder:
                    l_reminder = log_reminder(True)
                if not self.dry_run:
                    pass
                    # send_mail(person['activity__person__first_name'],
                    #           person['activity__person__last_name'],
                    #           person['activity__person__email'],
                    #           first_day_in_month,
                    #           last_day_in_month,
                    #           current_site.domain,
                    #           self.reminder,
                    #           self.log_file)
            else :
                l_timesheet = log_timehseet(True)

            self.logger.info(l_head, l_reminder + l_timesheet + l_person)

        self.logger.info("", "-----------------------------------------------------")

def log_head(first_day_in_month, last_day_in_month):
    return first_day_in_month.strftime('%Y/%m/%d') + " - "+ last_day_in_month.strftime('%Y/%m/%d')


def log_reminder(b=False):
    return "Reminder : " + checkboxes[str(b)] + " | "


def log_timehseet(b=False):
    return "Timesheet : " + checkboxes[str(b)] + " | "


def log_person(id, firstname, lastname, projects):
    p_str = "person id: "+id+" | " \
        + firstname + ' ' \
        + lastname
    for project_id, project_v in projects.items():
        p_str = p_str + " | project : " + project_v['name']
        if len(project_v['work_packages']):
            p_str = p_str +" "+str(project_v['work_packages'])
    return p_str


def send_mail(first_name, last_name, email, date_from, date_to, domain, is_reminder=False, log_file):
    subject = "[WWW] Veuillez saisir vos timesheets"
    to = (email,)
    from_email = settings.DEFAULT_FROM_EMAIL

    if is_reminder:
        subject = "[Rappel] " + subject
        to = to + (settings.TIMESHEET_MASTER_MAIL, )

    ctx = {
        'first_name': first_name,
        'last_name': last_name,
        'date_from': date_from,
        'date_to': date_to,
        'timesheet_url' : "https://"+ domain + reverse('organization-network-timesheet-create-view', args=(date_from.year, date_from.month))
    }

    message = get_template('email/timesheet.html').render(ctx)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.attach_file(log_file, "text/plain")
    msg.send()

    return HttpResponse('email_application_notification')
