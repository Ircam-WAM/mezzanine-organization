# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-13 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_media', '0006_auto_20161013_1631'),
        ('pages', '0005_auto_20160923_1219'),
        ('organization_pages', '0007_auto_20161007_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagePlaylist',
            fields=[
                ('playlist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='organization_media.Playlist')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='playlists', to='pages.Page', verbose_name='page')),
            ],
            options={
                'verbose_name': 'playlist',
                'verbose_name_plural': 'playlists',
            },
            bases=('organization_media.playlist',),
        ),
        migrations.DeleteModel(
            name='PageAudio',
        ),
        migrations.DeleteModel(
            name='PageVideo',
        ),
        migrations.AlterOrderWithRespectTo(
            name='pageplaylist',
            order_with_respect_to='page',
        ),
    ]
