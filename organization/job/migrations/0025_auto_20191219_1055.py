# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-12-19 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_job', '0024_auto_20191219_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidacy',
            name='text_button',
            field=models.CharField(blank=True, default='View', max_length=150, verbose_name='text button'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='text_button_en',
            field=models.CharField(blank=True, default='View', max_length=150, null=True, verbose_name='text button'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='text_button_fr',
            field=models.CharField(blank=True, default='View', max_length=150, null=True, verbose_name='text button'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='text_button',
            field=models.CharField(blank=True, default='View', max_length=150, verbose_name='text button'),
        ),
    ]
