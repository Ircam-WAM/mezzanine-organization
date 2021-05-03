# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-19 16:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization-magazine', '0027_auto_20190402_1502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': (('user_edit', 'User can edit its own content'), ('user_delete', 'User can delete its own content'), ('team_edit', "User can edit his team's content"), ('team_delete', "User can delete his team's content")), 'verbose_name': 'article'},
        ),
    ]
