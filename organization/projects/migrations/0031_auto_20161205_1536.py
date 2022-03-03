# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-05 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0030_auto_20161107_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('logo_white', 'logo white'), ('logo_black', 'logo black'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured')], max_length=64, verbose_name='type'),
        ),
    ]
