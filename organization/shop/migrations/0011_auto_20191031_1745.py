# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-10-31 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20190703_1044'),
        ('organization_shop', '0010_teamproduct'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductPrestashopProduct',
            new_name='ProductExternalShop'
        )
    ]
