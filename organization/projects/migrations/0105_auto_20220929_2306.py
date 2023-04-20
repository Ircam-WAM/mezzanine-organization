# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-09-29 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0104_auto_20220922_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_readme_in_repo',
            field=models.BooleanField(default=True, help_text='If the README is added to the repository.', verbose_name='is readme in repository'),
        ),
        migrations.AddField(
            model_name='project',
            name='readme_cms_content',
            field=models.TextField(blank=True, null=True, verbose_name='readme content from cms'),
        ),
    ]
