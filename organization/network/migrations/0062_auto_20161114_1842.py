# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-14 17:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0061_auto_20161114_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personactivity',
            options={'ordering': ['-date_from'], 'verbose_name': 'activity', 'verbose_name_plural': 'activities'},
        ),
    ]
