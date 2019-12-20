# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-19 18:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization-job', '0017_auto_20190130_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joboffer',
            options={'permissions': (('user_edit', 'Mezzo - User can edit its own content'), ('user_delete', 'Mezzo - User can delete its own content'), ('team_edit', "Mezzo - User can edit his team's content"), ('team_delete', "Mezzo - User can delete his team's content")), 'verbose_name': 'job offer', 'verbose_name_plural': 'job offers'},
        ),
        migrations.AddField(
            model_name='joboffer',
            name='user',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='joboffers', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
            preserve_default=False,
        ),
    ]