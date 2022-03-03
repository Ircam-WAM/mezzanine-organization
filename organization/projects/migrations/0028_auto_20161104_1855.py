# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-04 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0027_auto_20161104_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectrelatedtitle',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='projectrelatedtitle',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
    ]
