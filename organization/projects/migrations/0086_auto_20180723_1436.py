# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-07-23 12:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization-projects', '0085_auto_20180709_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pivot_projecttopic_article',
            options={'ordering': ('_order',), 'verbose_name': 'Project Topic'},
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_projects', to=settings.AUTH_USER_MODEL, verbose_name='project owner'),
        ),
        migrations.AlterField(
            model_name='pivot_projecttopic_article',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_topics_pivot', to='organization-magazine.Article', verbose_name='article'),
        ),
    ]
