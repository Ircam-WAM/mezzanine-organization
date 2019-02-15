# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-02-04 09:40
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0092_auto_20181228_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='configuration',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]