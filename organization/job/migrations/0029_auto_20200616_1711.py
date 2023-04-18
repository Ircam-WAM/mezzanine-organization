# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-06-16 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_job', '0028_auto_20191219_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobresponse',
            options={'verbose_name': 'job reponse', 'verbose_name_plural': 'job reponses'},
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='type',
            field=models.CharField(blank=True, choices=[('internship', 'Internship'), ('job', 'Permanent position'), ('short_term_contract', 'Short term contract')], max_length=32, verbose_name='Job offer type'),
        ),
    ]
