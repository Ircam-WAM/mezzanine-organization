# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-12-19 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-job', '0025_auto_20191219_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidacy',
            name='external_content',
        ),
        migrations.RemoveField(
            model_name='joboffer',
            name='external_content',
        ),
        migrations.AddField(
            model_name='candidacy',
            name='url',
            field=models.URLField(blank=True, help_text='If definied, it will redirect to this url, by default, it will display content of this page.', max_length=1000, verbose_name='external content'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='url',
            field=models.URLField(blank=True, help_text='If definied, it will redirect to this url, by default, it will display content of this page.', max_length=1000, verbose_name='external content'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='text_button',
            field=models.CharField(blank=True, max_length=150, verbose_name='text button'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='text_button_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='text button'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='text_button_fr',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='text button'),
        ),
    ]
