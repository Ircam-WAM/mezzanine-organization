# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-16 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0009_auto_20160916_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='personactivity',
            name='weeks',
            field=models.IntegerField(blank=True, null=True, verbose_name='number of weeks'),
        ),
    ]
