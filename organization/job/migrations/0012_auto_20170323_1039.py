# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-23 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_job', '0011_auto_20170105_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidacy',
            name='date_from',
            field=models.DateField(blank=True, null=True, verbose_name='start date'),
        ),
    ]
