# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-16 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0007_auto_20160907_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSubTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'project sub topic',
            },
        ),
        migrations.CreateModel(
            name='ProjectTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'project topic',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='sub_topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='organization_projects.ProjectSubTopic', verbose_name='sub topic'),
        ),
        migrations.AddField(
            model_name='project',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='organization_projects.ProjectTopic', verbose_name='topic'),
        ),
    ]
