# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-11-05 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-shop', '0014_auto_20191105_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='productexternalshop',
            name='label',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='label'),
        ),
    ]
