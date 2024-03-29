# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-14 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0086_auto_20170118_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationblock',
            name='background_color',
            field=models.CharField(blank=True, choices=[('black', 'black'), ('yellow', 'yellow'), ('red', 'red'), ('white', 'white')], max_length=32, verbose_name='background color'),
        ),
        migrations.AlterField(
            model_name='personblock',
            name='background_color',
            field=models.CharField(blank=True, choices=[('black', 'black'), ('yellow', 'yellow'), ('red', 'red'), ('white', 'white')], max_length=32, verbose_name='background color'),
        ),
    ]
