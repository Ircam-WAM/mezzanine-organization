# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-21 13:07
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0042_auto_20161021_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.TextField(blank=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='postal_code',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='postal code'),
        ),
    ]
