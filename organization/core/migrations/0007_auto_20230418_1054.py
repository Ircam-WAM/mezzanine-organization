# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-04-18 08:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_core', '0006_auto_20230417_1633'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metacategory',
            options={'verbose_name': 'meta category'},
        ),
    ]
