# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-04-18 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-agenda', '0026_auto_20170313_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventtraining',
            name='language',
            field=models.CharField(blank=True, choices=[('fr', 'French'), ('en', 'English')], max_length=64, null=True, verbose_name='language'),
        ),
    ]