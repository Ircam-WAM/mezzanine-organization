# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-04-17 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_core', '0005_linktype_fa_option'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomCategory',
            new_name='MetaCategory',
        ),
        migrations.AlterModelOptions(
            name='metacategory',
            options={'verbose_name': 'meta category', 'verbose_name_plural': 'meta categories'},
        ),
    ]