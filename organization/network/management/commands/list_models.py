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

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.apps import apps


class Command(BaseCommand):
    help = """list models + properties per apps
    """

    def handle(self, *args, **options):
        # process active person
        translation.activate(settings.LANGUAGE_CODE)
        applications = [
            'organization_network',
            'organization_projects'
        ]
        for app in applications:
            print(str(_(app)))
            models = apps.all_models[app]
            tab = "	"
            for model_str, model in models.items():
                print(tab + model_str + tab + str(_(model._meta.verbose_name)))
                fields = model._meta.get_fields()
                for field in fields:
                    field_str = ""
                    try:
                        field_str += tab + tab + tab + field.attname
                        # field_str += tab + str(field.verbose_name)
                        field_str += tab + str(_(field.verbose_name))
                    except AttributeError:
                        pass
                    if field_str:
                        print(field_str)
            translation.deactivate()
