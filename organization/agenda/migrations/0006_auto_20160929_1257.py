# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-29 10:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_media', '0001_initial'),
        ('organization_agenda', '0005_auto_20160928_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventaudio',
            options={'verbose_name': 'audio', 'verbose_name_plural': 'audios'},
        ),
        migrations.AlterModelOptions(
            name='eventvideo',
            options={'verbose_name': 'video', 'verbose_name_plural': 'videos'},
        ),
        migrations.AddField(
            model_name='eventaudio',
            name='audio_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, serialize=False, to='organization_media.Audio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventvideo',
            name='video_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, serialize=False, to='organization_media.Video'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='_order',
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='credits',
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='description',
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='file',
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='id',
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='title',
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='type',
        ),
        migrations.AlterOrderWithRespectTo(
            name='eventaudio',
            order_with_respect_to='event',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='_order',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='credits',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='description',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='file',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='id',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='title',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='type',
        ),
        migrations.AlterOrderWithRespectTo(
            name='eventvideo',
            order_with_respect_to='event',
        ),
    ]
