# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-10-18 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0094_person_karma'),
    ]

    operations = [
        migrations.AddField(
            model_name='personlistblock',
            name='label',
            field=models.CharField(default='', max_length=1024, verbose_name='label'),
            preserve_default=False,
        ),
    ]
