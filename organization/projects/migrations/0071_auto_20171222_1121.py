# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-12-22 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0070_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontentproject',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_content_project', to='organization_projects.Project', verbose_name='project'),
        ),
    ]
