# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-05 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0034_organization_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.TextField(verbose_name='address'),
        ),
    ]
