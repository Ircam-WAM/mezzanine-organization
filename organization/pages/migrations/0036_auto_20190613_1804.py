# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-13 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-pages', '0035_custompage_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custompage',
            options={'ordering': ('_order',), 'permissions': (('user_edit', 'User can edit its own content'), ('user_delete', 'User can delete its own content'), ('team_edit', "User can edit his team's content"), ('team_delete', "User can delete his team's content")), 'verbose_name': 'custom page'},
        ),
    ]
