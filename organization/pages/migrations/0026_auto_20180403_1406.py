# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-04-03 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-pages', '0025_auto_20171222_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
            preserve_default=False,
        ),
    ]
