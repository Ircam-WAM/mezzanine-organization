# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-11-04 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_agenda', '0039_externalshop_content'),
        ('organization-shop', '0012_auto_20191104_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productexternalshop',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='productexternalshop',
            name='url',
        ),
        migrations.AddField(
            model_name='productexternalshop',
            name='shop',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_external_shop', to='mezzanine_agenda.ExternalShop', verbose_name='shop'),
        ),
    ]
