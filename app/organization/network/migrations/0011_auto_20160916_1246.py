# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-16 10:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0010_personactivity_weeks'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='code',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='personactivity',
            name='umr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization-network.UMR', verbose_name='UMR'),
        ),
    ]
