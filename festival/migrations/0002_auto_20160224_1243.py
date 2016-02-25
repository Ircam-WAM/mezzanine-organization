# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='bio_en',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='bio_fr',
        ),
        migrations.AddField(
            model_name='artist',
            name='content',
            field=mezzanine.core.fields.RichTextField(default='', verbose_name='Content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artist',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='artist',
            name='content_fr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='video',
            name='event',
            field=models.ForeignKey(related_name='videos', on_delete=django.db.models.deletion.SET_NULL, verbose_name='event', blank=True, to='mezzanine_agenda.Event', null=True),
        ),
    ]
