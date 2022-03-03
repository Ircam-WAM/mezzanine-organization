# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('title_fr', models.CharField(max_length=1024, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=1024, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('media_id', models.CharField(max_length=128, verbose_name='media id')),
                ('open_source_url', models.URLField(blank=True, max_length=1024, verbose_name='open source URL')),
                ('closed_source_url', models.URLField(blank=True, max_length=1024, verbose_name='closed source URL')),
                ('poster_url', models.URLField(blank=True, max_length=1024, verbose_name='poster')),
            ],
            options={
                'verbose_name': 'audio',
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('audios', models.ManyToManyField(blank=True, related_name='playlists', to='organization_media.Audio', verbose_name='audios')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='title')),
                ('title_fr', models.CharField(max_length=1024, null=True, verbose_name='title')),
                ('title_en', models.CharField(max_length=1024, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='description')),
                ('media_id', models.CharField(max_length=128, verbose_name='media id')),
                ('open_source_url', models.URLField(blank=True, max_length=1024, verbose_name='open source URL')),
                ('closed_source_url', models.URLField(blank=True, max_length=1024, verbose_name='closed source URL')),
                ('poster_url', models.URLField(blank=True, max_length=1024, verbose_name='poster')),
            ],
            options={
                'verbose_name': 'video',
            },
        ),
        migrations.CreateModel(
            name='VideoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name': 'video category',
            },
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='organization_media.VideoCategory', verbose_name='category'),
        ),
    ]
