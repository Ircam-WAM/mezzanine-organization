# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-19 18:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-network', '0138_auto_20190619_2047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'permissions': (('user_edit', 'Mezzo - User - User can edit its own content'), ('user_delete', 'Mezzo - User - User can delete its own content'), ('team_edit', "Mezzo - Team - User can edit his team's content"), ('team_delete', "Mezzo - Team - User can delete his team's content")), 'verbose_name': 'organization'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['last_name'], 'permissions': (('user_edit', 'Mezzo - User - User can edit its own content'), ('user_delete', 'Mezzo - User - User can delete its own content'), ('team_edit', "Mezzo - Team - User can edit his team's content"), ('team_delete', "Mezzo - Team - User can delete his team's content")), 'verbose_name': 'person'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['name'], 'permissions': (('user_edit', 'Mezzo - User - User can edit its own content'), ('user_delete', 'Mezzo - User - User can delete its own content'), ('team_edit', "Mezzo - Team - User can edit his team's content"), ('team_delete', "Mezzo - Team - User can delete his team's content")), 'verbose_name': 'team'},
        ),
        migrations.AlterModelOptions(
            name='teampage',
            options={'ordering': ('_order',), 'permissions': (('user_edit', 'Mezzo - User - User can edit its own content'), ('user_delete', 'Mezzo - User - User can delete its own content'), ('team_edit', "Mezzo - Team - User can edit his team's content"), ('team_delete', "Mezzo - Team - User can delete his team's content")), 'verbose_name': 'team page'},
        ),
    ]
