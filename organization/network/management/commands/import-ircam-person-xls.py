import os
import sys
import csv
import logging
import datetime
from optparse import make_option
import xlrd
from itertools import takewhile

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from organization.core.models import *
from organization.network.models import *
from organization.projects.models import *


class Logger:

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def info(self, prefix, message):
        self.logger.info(' ' + prefix + ' : ' + message.decode('utf8'))

    def error(self, prefix, message):
        self.logger.error(prefix + ' : ' + message.decode('utf8'))


def get_instance(model, field, value):
    models = model.objects.filter(field=value)
    if models:
        return models[0]
    else:
        model = model()
        model.field = value
        return model


class IrcamXLS:

    sheet_id = 2
    first_row = 20

    def __init__(self, file):
        self.book = xlrd.open_workbook(file)
        self.sheet = self.book.sheet_by_index(self.sheet_id)
        self.size = self.column_len(0)

    def column_len(self, index):
        col_values = self.sheet.col_values(index)
        col_len = len(col_values)
        for _ in takewhile(lambda x: not x, reversed(col_values)):
            col_len -= 1
        return col_len

class IrcamPerson(object):

    organization = Organization.objects.get(name='Ircam')

    def __init__(self, row, datemode):
        self.row = row
        self.datemode = datemode
        last_name = self.row[0].value
        first_name = self.row[1].value
        print(last_name)
        title = ' '.join((first_name, last_name))

        self.person, c = Person.objects.get_or_create(title=title, first_name=first_name, last_name=last_name)
        self.activity = PersonActivity(person=self.person)

    def get_identity(self, ):
        gender = self.row[2].value
        if gender == 'H':
            self.person.gender = 'male'
        elif gender == 'F':
            self.person.gender = 'female'

        birthday = self.row[3].value
        if birthday:
            self.person.birthday = datetime.datetime(*xlrd.xldate_as_tuple(birthday, self.datemode))

        # self.person.nationality = self.get_or_create_name(Nationality, self.row[33].value)

        self.person.save()

    def get_or_create_name(self, model, column_id):
        return model.objects.get_or_create(name=self.row[column_id].value)[0] if self.row[column_id].value else None

    def get_person(self, value):
        if value:
            name_exceptions = ['de', 'von']

            names = value.split(' / ')[0]
            names = names.split(' ')

            if names[0] == 'M.':
                names.remove('M.')

            if names[0] == 'Mm.':
                names.remove('Mm.')

            first_name = names[0].capitalize()

            last_name = []
            for name in names[1:]:
                if name:
                    if name[0] != '(' and not name in name_exceptions:
                        last_name.append(name.capitalize())
            last_name = ' '.join(last_name)

            title = ' '.join((first_name, last_name))
            person, c = Person.objects.get_or_create(title=title)

            return person

        return None

    def get_activity(self):
        self.activity.date_from = datetime.datetime(*xlrd.xldate_as_tuple(self.row[4].value, self.datemode)) if self.row[4].value else None
        self.activity.date_to = datetime.datetime(*xlrd.xldate_as_tuple(self.row[5].value, self.datemode)) if self.row[5].value else None
        try:
            self.activity.weeks = int(self.row[6].value) if self.row[6].value else None
        except:
            pass

        self.activity.status = self.get_or_create_name(ActivityStatus, 10)
        self.activity.is_permanent = True if self.row[11].value else False
        self.activity.framework = self.get_or_create_name(ActivityFramework, 12)
        self.activity.grade = self.get_or_create_name(ActivityGrade, 13)

        self.activity.employer = self.get_or_create_name(Organization, 14)
        self.activity.attachment_organization = self.get_or_create_name(Organization, 15)
        self.activity.second_employer = self.get_or_create_name(Organization, 16)
        self.activity.umr = self.get_or_create_name(UMR, 17)

        self.activity.team, c = Team.objects.get_or_create(code=self.row[19].value, organization=self.organization) if self.row[19].value else (None, False)
        self.activity.second_team, c = Team.objects.get_or_create(code=self.row[21].value, organization=self.organization) if self.row[21].value else (None, False)
        self.activity.project, c = Project.objects.get_or_create(title=self.row[22].value) if self.row[22].value else (None, False)

        quota = self.row[23].value
        try:
            self.activity.rd_quota_float = float(quota)
        except:
            self.activity.rd_quota_text = str(quota)

        self.activity.phd_doctoral_school = self.get_or_create_name(Organization, 25)
        self.activity.phd_director = self.get_person(self.row[26].value)
        self.activity.phd_officer_1 = self.get_person(self.row[27].value)
        self.activity.phd_officer_2 = self.get_person(self.row[28].value)

        self.activity.training_type = self.get_or_create_name(TrainingType, 29)
        self.activity.training_level = self.get_or_create_name(TrainingLevel, 30)
        self.activity.training_topic = self.get_or_create_name(TrainingTopic, 31)
        self.activity.training_speciality = self.get_or_create_name(TrainingSpectiality, 32)
        self.activity.function = self.get_or_create_name(ActivityFunction, 34)

        if self.activity.phd_director:
            self.activity.phd_title = self.row[35].value
            try:
                self.activity.phd_defense_date = datetime.datetime(*xlrd.xldate_as_tuple(self.row[38].value, self.datemode)) if self.row[38].value else None
            except:
                pass
            self.activity.phd_postdoctoralsituation = self.row[39].value
        elif self.activity.training_type:
            self.activity.training_title = self.row[35].value

        self.activity.rd_program = self.row[36].value
        self.activity.comments = self.row[37].value
        self.activity.hdr = self.row[40].value
        self.activity.budget_code = self.get_or_create_name(BudgetCode, 41)
        self.activity.date_modified_manual = datetime.datetime(*xlrd.xldate_as_tuple(self.row[42].value, self.datemode)) if self.row[42].value else None
        self.activity.record_piece = self.get_or_create_name(RecordPiece, 43) if self.row[43].value else None

        self.activity.save()


class Command(BaseCommand):
    help = """Import Person data from IRCAM's legacy XLS management file"""

    option_list = BaseCommand.option_list + (
          make_option('-d', '--dry-run',
            action='store_true',
            dest='dry-run',
            help='Do NOT write anything'),
          make_option('-f', '--force',
            action='store_true',
            dest='force',
            help='Force overwrite data'),
          make_option('-s', '--source',
            dest='source_file',
            help='define the XLS source file'),
          make_option('-l', '--log',
            dest='log',
            help='define log file'),
    )

    def handle(self, *args, **kwargs):
        # self.logger = Logger(kwargs.get('log'))
        self.pattern = kwargs.get('pattern')
        self.source_file = os.path.abspath(kwargs.get('source_file'))
        self.dry_run =  kwargs.get('dry-run')
        self.force = kwargs.get('force')

        xls = IrcamXLS(self.source_file)
        for i in range(xls.first_row, xls.size):
            p = IrcamPerson(xls.sheet.row(i), xls.book.datemode)
            p.get_identity()
            p.get_activity()
