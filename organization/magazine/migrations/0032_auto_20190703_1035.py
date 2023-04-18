# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-07-03 08:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_magazine', '0031_auto_20190619_2052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'permissions': (('user_add', 'Mezzo - User - User can add its own content'), ('user_edit', 'Mezzo - User - User can edit its own content'), ('user_delete', 'Mezzo - User - User can delete its own content'), ('team_add', 'Mezzo - User - Team can add its own content'), ('team_edit', "Mezzo - Team - User can edit his team's content"), ('team_delete', "Mezzo - Team - User can delete his team's content")), 'verbose_name': 'article'},
        ),
        migrations.AlterModelOptions(
            name='brief',
            options={'permissions': (('user_add', 'Mezzo - User - User can add its own content'), ('user_edit', 'Mezzo - User - User can edit its own content'), ('user_delete', 'Mezzo - User - User can delete its own content'), ('team_add', 'Mezzo - User - Team can add its own content'), ('team_edit', "Mezzo - Team - User can edit his team's content"), ('team_delete', "Mezzo - Team - User can delete his team's content")), 'verbose_name': 'brief'},
        ),
    ]
