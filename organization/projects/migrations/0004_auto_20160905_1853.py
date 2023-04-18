# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 16:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0003_auto_20160901_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'project programme',
            },
        ),
        migrations.CreateModel(
            name='ProjectProgramType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'project programme type',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('research topic', 'research topic'), ('collaborative project', 'collaborative project')], default=1, max_length=128, verbose_name='type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='partner_projects', to='organization_network.Team', verbose_name='teams'),
        ),
        migrations.AddField(
            model_name='project',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='organization_projects.ProjectProgram', verbose_name='project program'),
        ),
        migrations.AddField(
            model_name='project',
            name='program_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='organization_projects.ProjectProgramType', verbose_name='project program type'),
        ),
    ]
