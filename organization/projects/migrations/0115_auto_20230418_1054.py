# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-04-18 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0114_project_meta_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='meta_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='organization-core.MetaCategory', verbose_name='meta category'),
        ),
    ]
