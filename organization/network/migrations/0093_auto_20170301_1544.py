# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-01 14:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0092_auto_20170228_1317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personactivitytimesheet',
            options={'ordering': ['-year', 'month', 'project'], 'verbose_name': 'activity timesheet', 'verbose_name_plural': 'activity timesheets'},
        ),
    ]
