# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-10-26 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_media', '0025_auto_20190703_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='external_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='media id'),
        ),
    ]