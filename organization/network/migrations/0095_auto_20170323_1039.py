# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-23 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0094_auto_20170323_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personactivity',
            name='date_from',
            field=models.DateField(blank=True, null=True, verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='personactivityvacation',
            name='date_from',
            field=models.DateField(blank=True, null=True, verbose_name='start date'),
        ),
    ]
