# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-04-03 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0073_auto_20180306_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='project_topics', to='organization-projects.ProjectTopic', verbose_name='topics'),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectblogpage',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectcall',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectcollection',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectdemo',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectresidency',
            name='slug',
            field=models.CharField(blank=True, default='', help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, verbose_name='URL'),
            preserve_default=False,
        ),
    ]
