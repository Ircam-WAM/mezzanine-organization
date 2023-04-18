# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-21 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0119_remove_team_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='hal_url',
            field=models.URLField(blank=True, max_length=512, verbose_name='HAL url'),
        ),
    ]
