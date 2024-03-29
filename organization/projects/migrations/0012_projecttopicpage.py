# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-22 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20160804_1547'),
        ('organization_projects', '0011_auto_20160922_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTopicPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Page')),
                ('sub_title', models.TextField(blank=True, max_length=1024, verbose_name='sub title')),
                ('project_topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='organization_projects.ProjectTopic', verbose_name='project topic')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'team page',
            },
            bases=('pages.page', models.Model),
        ),
    ]
