# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-03-22 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0092_auto_20170314_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='organization_name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='organization_name'),
        ),
        migrations.AddField(
            model_name='person',
            name='position',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='position'),
        ),
    ]
