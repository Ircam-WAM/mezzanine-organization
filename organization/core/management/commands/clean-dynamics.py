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
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


def clean_dynamics(app, model, parent_prpty, dl):

    DynamicContentModel = apps.get_model(app, model)
    delete_with_no_ancestors(app, DynamicContentModel, parent_prpty, dl)
    delete_with_no_descendent(app, DynamicContentModel, dl)


def delete_with_no_ancestors(app, DynamicContentModel, parent_prpty, dl):
    print("******************************************")
    print(
        ">>>> These orphans '" +
        DynamicContentModel.__name__ +
        "' dynamic content will be DELETED"
    )
    print("******************************************")
    kwargs = {
        '{0}__{1}'.format(parent_prpty, 'isnull'): True,
    }
    dynamic_contents = DynamicContentModel.objects.filter(**kwargs)
    for dc in dynamic_contents:
        print("Parent - content null", dc.id)
        if dl:
            dc.delete()


def delete_with_no_descendent(app, DynamicContentModel, dl):
    print("******************************************")
    print(
        ">>>> test if related contents in '" +
        DynamicContentModel.__name__ +
        "' (children) still exist "
    )
    print("******************************************")
    dynamic_contents = DynamicContentModel.objects.all()
    for dc in dynamic_contents:
        try:
            ct = ContentType.objects.get(id=dc.content_type_id)
        except ObjectDoesNotExist:
            print(
                "children - Content Type '" +
                str(dc.content_type_id) +
                "' NOT exists with id ",
                dc.object_id,
                "| dynamic ",
                ct.model,
                ">>>>> WILL BE DELETED"
            )
            if dl:
                dc.delete()
        model = apps.get_model(ct.app_label, ct.model)
        try:
            obj = model.objects.get(id=dc.object_id)
            print("children - exits", obj.id, ct.model)
        except ObjectDoesNotExist:
            print(
                "children - NOT exists with id ",
                dc.object_id,
                '| dynamic',
                ct.model,
                ">>>>> WILL BE DELETED"
            )
            # for some misterious reasons, id of some objects are None,
            # so we can't delete them
            # then we set a temp dummy id before deleting them
            if not dc.id:
                dc.id = 99999
                dc.save()
            if dl:
                dc.delete()


class Command(BaseCommand):

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Do NOT write anything',
        )

    def handle(self, *args, **options):
        self.delete = options['delete']

        clean_dynamics(
            'organization-magazine',
            'DynamicContentArticle',
            'article_id',
            self.delete
        )
        clean_dynamics(
            'organization-pages',
            'DynamicContentPage',
            'page_id',
            self.delete
        )
        clean_dynamics(
            'organization-agenda',
            'DynamicContentEvent',
            'event_id',
            self.delete
        )
        clean_dynamics(
            'organization-pages',
            'DynamicContentHomeSlider',
            'home_id',
            self.delete
        )
        clean_dynamics(
            'organization-pages',
            'DynamicContentHomeBody',
            'home_id',
            self.delete
        )
        clean_dynamics(
            'organization-pages',
            'DynamicContentHomeMedia',
            'home_id',
            self.delete
        )
        clean_dynamics(
            'organization-projects',
            'DynamicContentProject',
            'project_id',
            self.delete
        )
