# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-28 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0003_auto_20160923_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageimage',
            name='type',
            field=models.CharField(choices=[('logo', 'logo'), ('slider', 'slider'), ('card', 'card'), ('page_slider', 'page - slider'), ('page_featured', 'page - featured')], max_length=64, verbose_name='type'),
        ),
    ]
