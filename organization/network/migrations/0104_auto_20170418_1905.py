# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-04-18 17:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0103_organizationrole_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizationrole',
            options={'ordering': ['key'], 'verbose_name': 'organization role'},
        ),
    ]
