# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from organization.network.models import PersonActivity, ProjectActivity

def migrate_project(apps, schema_editor):
    activities = PersonActivity.objects.all()
    for activity in activities :
        for project in activity.projects.all() :
            pa = ProjectActivity()
            pa.title = activity.person.title
            pa.project = project
            pa.activity = activity
            pa.save()


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0087_auto_20170127_1708'),
    ]

    operations = [
    	migrations.RunPython(migrate_project),
    ]
