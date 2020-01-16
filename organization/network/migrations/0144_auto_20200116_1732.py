# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-01-16 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0143_person_account_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='account_type',
            field=models.IntegerField(choices=[(0, 'Individual'), (1, 'Organization')], default=0, null=True, verbose_name='account type'),
        ),
    ]
