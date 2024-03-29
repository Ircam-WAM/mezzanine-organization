# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-06 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0079_auto_20170106_1149'),
        ('organization_projects', '0034_auto_20161230_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.ManyToManyField(blank=True, null=True, related_name='projects_manager', to='organization_network.Person', verbose_name='Manager'),
        ),
        migrations.AddField(
            model_name='project',
            name='referring_person',
            field=models.ManyToManyField(blank=True, null=True, related_name='projects_referring_person', to='organization_network.Person', verbose_name='Referring Person'),
        ),
    ]
