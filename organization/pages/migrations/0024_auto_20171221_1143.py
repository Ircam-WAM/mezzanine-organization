# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-12-21 10:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-pages', '0023_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontentpage',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_content_pages', to='pages.Page', verbose_name='page'),
        ),
    ]
