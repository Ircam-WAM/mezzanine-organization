# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-23 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0023_auto_20160921_2043'),
        ('organization_projects', '0014_auto_20160922_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lead_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader_projects', to='organization_network.Organization', verbose_name='lead organization'),
        ),
    ]
