# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-07-13 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_magazine', '0019_auto_20170105_1743'),
        ('organization_projects', '0062_auto_20170710_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectResidencyArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='residencies', to='organization_magazine.Article', verbose_name='article')),
                ('residency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='organization_projects.ProjectResidency', verbose_name='residency')),
            ],
        ),
    ]
