# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-08 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0055_activitystatus_display_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitystatus',
            name='display_text',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='display text'),
        ),
    ]
