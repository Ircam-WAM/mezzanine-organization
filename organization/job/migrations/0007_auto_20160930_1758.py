# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-30 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_job', '0006_candidacyimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidacy',
            name='text_button',
        ),
        migrations.RemoveField(
            model_name='candidacy',
            name='text_button_en',
        ),
        migrations.RemoveField(
            model_name='candidacy',
            name='text_button_fr',
        ),
        migrations.AddField(
            model_name='candidacy',
            name='date_from',
            field=models.DateField(blank=True, null=True, verbose_name='begin date'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='date_to',
            field=models.DateField(blank=True, null=True, verbose_name='end date'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='text_button_external',
            field=models.CharField(blank=True, max_length=150, verbose_name='external text button'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='text_button_external_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='external text button'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='text_button_external_fr',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='external text button'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='text_button_internal',
            field=models.CharField(blank=True, max_length=150, verbose_name='internal text button'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='text_button_internal_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='internal text button'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='text_button_internal_fr',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='internal text button'),
        ),
    ]
