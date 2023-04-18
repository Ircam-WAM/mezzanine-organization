# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-28 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0014_auto_20161028_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagerelatedtitle',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='pagerelatedtitle',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
    ]
