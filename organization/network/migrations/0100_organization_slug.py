# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-04-07 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0099_organization_validation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='slug',
            field=models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the name.', max_length=2000, null=True, verbose_name='URL'),
        ),
    ]
