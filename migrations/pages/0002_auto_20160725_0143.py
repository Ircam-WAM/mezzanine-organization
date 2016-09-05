# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 23:43
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.pages.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='in_menus',
            field=mezzanine.pages.fields.MenusField(blank=True, choices=[(1, 'Action'), (2, 'Departement'), (3, 'Footer vertical'), (4, 'Footer horizontal')], max_length=100, null=True, verbose_name='Show in menus'),
        ),
    ]