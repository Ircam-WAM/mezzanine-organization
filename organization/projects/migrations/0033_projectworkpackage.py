# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-28 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0073_auto_20161228_1428'),
        ('organization_projects', '0032_project_external_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectWorkPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='begin date')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='end date')),
                ('number', models.IntegerField(verbose_name='number')),
                ('lead_organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader_work_packages', to='organization_network.Organization', verbose_name='lead organization')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_packages', to='organization_projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'work package',
                'ordering': ['number'],
                'verbose_name_plural': 'work packages',
            },
        ),
    ]
