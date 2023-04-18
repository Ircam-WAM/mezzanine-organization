# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-12-19 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_job', '0027_jobofferimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidacy',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='text_button_en',
            field=models.CharField(blank=True, default='View', max_length=150, null=True, verbose_name='text button'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='text_button_fr',
            field=models.CharField(blank=True, default='View', max_length=150, null=True, verbose_name='text button'),
        ),
    ]
