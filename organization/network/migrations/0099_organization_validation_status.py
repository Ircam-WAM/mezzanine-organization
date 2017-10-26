# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-04-07 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0098_producerdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='validation_status',
            field=models.IntegerField(choices=[(0, 'rejected'), (1, 'pending'), (2, 'in process'), (3, 'accepted')], default=1, verbose_name='validation status'),
        ),
    ]