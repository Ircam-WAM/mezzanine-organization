# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-07 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization-core', '0009_pageblock_with_separator'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('slug', models.SlugField(blank=True, help_text='Use this field to define a simple identifier that can be used to style the different link types (i.e. assign social media icons to them)', max_length=256, verbose_name='slug')),
                ('ordering', models.PositiveIntegerField(blank=True, null=True, verbose_name='ordering')),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
        migrations.AlterModelOptions(
            name='pageimage',
            options={'ordering': ('_order',), 'verbose_name': 'image', 'verbose_name_plural': 'images'},
        ),
    ]
