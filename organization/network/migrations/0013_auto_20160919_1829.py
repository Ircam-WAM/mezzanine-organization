# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-19 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0002_auto_20160914_1838'),
        ('organization_network', '0012_auto_20160916_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageCustomPersonListBlockInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_list_block', to='organization_pages.CustomPage', verbose_name='Page')),
            ],
            options={
                'verbose_name': 'Person List',
            },
        ),
        migrations.CreateModel(
            name='PersonListBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('style', models.CharField(choices=[('square', 'square'), ('circle', 'circle')], max_length=16, verbose_name='style')),
            ],
            options={
                'verbose_name': 'Person List',
            },
        ),
        migrations.CreateModel(
            name='PersonListBlockInline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_list_block', to='organization_network.Person', verbose_name='Person')),
                ('person_list_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_autocomplete', to='organization_network.PersonListBlock', verbose_name='Person List Block')),
            ],
            options={
                'verbose_name': 'Person autocomplete',
            },
        ),
        migrations.AddField(
            model_name='pagecustompersonlistblockinline',
            name='person_list_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_custom', to='organization_network.PersonListBlock', verbose_name='Person List Block'),
        ),
    ]
