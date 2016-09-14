# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-14 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20160804_1547'),
        ('organization-core', '0002_linktype_picto'),
        ('organization-pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, max_length=512, verbose_name='URL')),
                ('link_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization-core.LinkType', verbose_name='link type')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to='pages.Page', verbose_name='page')),
            ],
            options={
                'verbose_name_plural': 'links',
                'verbose_name': 'link',
            },
        ),
        migrations.AlterOrderWithRespectTo(
            name='pagelink',
            order_with_respect_to='page',
        ),
    ]
