# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-10-25 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0095_personlistblock_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='hal_researche_structure',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='HAL Researche Structure'),
        ),
        migrations.AddField(
            model_name='team',
            name='hal_tutelage',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='HAL Tutelage'),
        ),
    ]
