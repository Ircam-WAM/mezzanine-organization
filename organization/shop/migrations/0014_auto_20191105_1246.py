# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-11-05 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_shop', '0013_auto_20191104_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productexternalshop',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_external_shop', to='mezzanine_agenda.ExternalShop', verbose_name='shop'),
        ),
    ]
