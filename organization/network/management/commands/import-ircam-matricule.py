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
import xlrd
from optparse import make_option
from django.core.management.base import BaseCommand
from organization.network.models import Person
from django.utils.text import slugify


class Command(BaseCommand):
    help = r"""Import register id from xlsx file
    python manage.py import-ircam-matricule -s /srv/backup/MatriculesIrcamR\&D_2015-2016.xlsx  # noqa: E501
    """
    option_list = BaseCommand.option_list + (
        make_option(
            '-s',
            '--source',
            dest='source_file',
            help='define the XLS source file'
        ),
    )
    number_of_person = 0
    number_of_person_non_processed = 0

    def handle(self, *args, **kwargs):

        self.source_file = os.path.abspath(kwargs.get('source_file'))
        self.book = xlrd.open_workbook(self.source_file)
        self.sheet = self.book.sheet_by_index(0)
        self.first_row = self.sheet.row(0)
        for row_idx in range(0, self.sheet.nrows):    # Iterate through rows
            cell_id = self.sheet.cell(row_idx, 0).value
            print("cell_id", type(cell_id), cell_id)
            if isinstance(cell_id, float):
                cell_id = str(int(cell_id))
            if isinstance(cell_id, str):
                cell_id = cell_id.strip()
            cell_last_name = self.sheet.cell(row_idx, 1).value
            cell_first_name = self.sheet.cell(row_idx, 2).value
            self.update_register_id(cell_id, cell_last_name, cell_first_name)

        print('***************************************************')
        print("Number of person processed : "+str(self.number_of_person))
        print('***************************************************')
        print("Number of person NON processed : " + str(
                self.number_of_person_non_processed
            )
        )
        print('***************************************************')

    def update_register_id(self, id, last_name, first_name):
        slug = slugify(first_name+'-'+last_name)
        person = Person.objects.filter(slug__contains=slug)
        if person:
            self.number_of_person += 1
            # persons have sometimes two ids
            for p in person:
                p.register_id = id
                p.save()
        else:
            print(
                "Person not found: " +
                last_name +
                ' ' +
                first_name +
                ' | manual slug : ' +
                slug
            )
            self.number_of_person_non_processed += 1
