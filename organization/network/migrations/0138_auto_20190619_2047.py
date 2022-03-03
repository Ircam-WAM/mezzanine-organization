# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-19 18:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0137_auto_20190619_2021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'permissions': (('user_edit', 'Mezzo - User can edit its own content'), ('user_delete', 'Mezzo - User can delete its own content'), ('team_edit', "Mezzo - User can edit his team's content"), ('team_delete', "Mezzo - User can delete his team's content")), 'verbose_name': 'organization'},
        ),
        migrations.AlterField(
            model_name='organization',
            name='user',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
            preserve_default=False,
        ),
    ]
