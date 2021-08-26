# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-11-05 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_shop', '0015_productexternalshop_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='productexternalshop',
            name='label_en',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='label'),
        ),
        migrations.AddField(
            model_name='productexternalshop',
            name='label_fr',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='label'),
        ),
    ]
