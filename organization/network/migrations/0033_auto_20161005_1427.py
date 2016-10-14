# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-05 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0032_auto_20161005_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='longitude',
        ),
        migrations.AddField(
            model_name='organization',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=7, help_text='Calculated automatically if mappable location is set.', max_digits=10, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='organization',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=7, help_text='Calculated automatically if mappable location is set.', max_digits=10, null=True, verbose_name='Longitude'),
        ),
        migrations.AddField(
            model_name='organization',
            name='mappable_location',
            field=models.CharField(blank=True, help_text='This address will be used to calculate latitude and longitude. Leave blank and set Latitude and Longitude to specify the location yourself, or leave all three blank to auto-fill from the Location field.', max_length=128),
        ),
    ]