# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-08 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0054_auto_20161107_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitystatus',
            name='display_text',
            field=models.CharField(blank=True, default=True, max_length=128, verbose_name='display text'),
        ),
    ]
