# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-18 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0085_auto_20170118_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personactivitytimesheet',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], verbose_name='month'),
        ),
    ]
