# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-27 18:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0088_auto_20170127_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personactivitytimesheet',
            options={'ordering': ['month', '-year'], 'verbose_name': 'activity timesheet', 'verbose_name_plural': 'activity timesheets'},
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='projects',
        ),
    ]
