# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-23 11:57
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.pages.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20160923_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='in_menus',
            field=mezzanine.pages.fields.MenusField(blank=True, choices=[(1, 'Action'), (2, 'Departement'), (3, 'Footer vertical'), (4, 'Footer horizontal'), (5, 'Magazine'), (6, 'Vous êtes'), (7, 'Personnes')], max_length=100, null=True, verbose_name='Show in menus'),
        ),
    ]