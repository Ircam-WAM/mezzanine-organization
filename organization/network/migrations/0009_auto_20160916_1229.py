# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-16 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0008_person_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personactivity',
            name='content',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='content_en',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='content_fr',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='description',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='personactivity',
            name='description_fr',
        ),
        migrations.AddField(
            model_name='personactivity',
            name='comments_en',
            field=models.TextField(blank=True, null=True, verbose_name='comments'),
        ),
        migrations.AddField(
            model_name='personactivity',
            name='comments_fr',
            field=models.TextField(blank=True, null=True, verbose_name='comments'),
        ),
    ]
