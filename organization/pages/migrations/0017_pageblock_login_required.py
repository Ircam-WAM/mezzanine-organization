# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-03 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0016_auto_20161205_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageblock',
            name='login_required',
            field=models.BooleanField(default=False, verbose_name='login required'),
        ),
    ]
