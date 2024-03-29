# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-22 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0010_auto_20160921_1934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['title'], 'verbose_name': 'project'},
        ),
        migrations.AlterModelOptions(
            name='projectprogram',
            options={'ordering': ['name'], 'verbose_name': 'program'},
        ),
        migrations.AlterModelOptions(
            name='projectprogramtype',
            options={'ordering': ['name'], 'verbose_name': 'program type'},
        ),
        migrations.AlterModelOptions(
            name='projecttopic',
            options={'ordering': ['name'], 'verbose_name': 'project topic'},
        ),
        migrations.AddField(
            model_name='projectprogram',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='projectprogram',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='projectprogram',
            name='name_en',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='projectprogram',
            name='name_fr',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='projectprogramtype',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='projectprogramtype',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='projectprogramtype',
            name='name_en',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='projectprogramtype',
            name='name_fr',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='projecttopic',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='projecttopic',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='projecttopic',
            name='name_en',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='projecttopic',
            name='name_fr',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
    ]
