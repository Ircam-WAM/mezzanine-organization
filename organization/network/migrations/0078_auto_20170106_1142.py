# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-06 10:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0077_auto_20170104_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personactivitytimesheet',
            name='accounting',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 1, 6, 10, 40, 49, 573524, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='personactivitytimesheet',
            name='validation',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 1, 6, 10, 40, 49, 573558, tzinfo=utc)),
        ),
    ]
