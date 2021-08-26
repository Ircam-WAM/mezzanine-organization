# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-03 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0046_auto_20161026_1025'),
        ('organization_projects', '0024_auto_20161103_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectdemo',
            name='author',
        ),
        migrations.RemoveField(
            model_name='projectdemo',
            name='directory',
        ),
        migrations.RemoveField(
            model_name='repositorysystem',
            name='type',
        ),
        migrations.AddField(
            model_name='projectdemo',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='demos', to='organization_network.Person', verbose_name='authors'),
        ),
        migrations.AddField(
            model_name='projectdemo',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='projectdemo',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='projectdemo',
            name='title_en',
            field=models.CharField(max_length=500, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='projectdemo',
            name='title_fr',
            field=models.CharField(max_length=500, null=True, verbose_name='Title'),
        ),
    ]
