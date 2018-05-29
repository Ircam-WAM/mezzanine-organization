# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-05-14 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0078_auto_20180503_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pivot_project_projectcollection',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collections_pivot', to='organization-projects.Project', verbose_name='project'),
        ),
    ]
