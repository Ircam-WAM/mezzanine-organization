# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-05 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0031_auto_20161005_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='latitude',
            field=models.CharField(blank=True, max_length=40, verbose_name='latitude'),
        ),
        migrations.AddField(
            model_name='organization',
            name='longitude',
            field=models.CharField(blank=True, max_length=40, verbose_name='longitude'),
        ),
    ]
