# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-06-08 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0083_auto_20180607_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_private',
            field=models.BooleanField(default=False, help_text='If the project is private, permissions will be enforced. Else, the project is considered public and they will be omitted.', verbose_name='Is private'),
        ),
    ]