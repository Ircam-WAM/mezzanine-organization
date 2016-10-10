# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-04 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0028_team_is_legacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='external_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='external ID'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='external_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='external ID'),
        ),
    ]