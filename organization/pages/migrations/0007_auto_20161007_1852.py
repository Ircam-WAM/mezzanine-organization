# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-07 16:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0006_auto_20161007_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontenthomemedia',
            name='home',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dynamic_content_home_media', to='organization_pages.Home', verbose_name='home'),
        ),
    ]
