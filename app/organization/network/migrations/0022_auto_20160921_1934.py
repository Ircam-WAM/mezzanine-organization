# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-21 17:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0021_auto_20160921_1908'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TrainingSpectiality',
            new_name='TrainingSpeciality',
        ),
    ]