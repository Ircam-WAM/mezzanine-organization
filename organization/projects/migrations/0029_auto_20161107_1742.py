# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-07 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0028_auto_20161104_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectdemo',
            name='directory',
            field=models.CharField(blank=True, help_text='Relative directory in repository', max_length=256, null=True, verbose_name='directory'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='url',
            field=models.CharField(help_text='(HTTP(S) or SSH)', max_length=256, verbose_name='URL'),
        ),
    ]
