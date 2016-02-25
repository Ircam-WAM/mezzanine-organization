# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_agenda', '0002_auto_20160224_1142'),
        ('festival', '0003_auto_20160224_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='FestivalEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eve_event_id', models.IntegerField(verbose_name='eve id', blank=True)),
                ('featured', models.BooleanField(default=False, verbose_name='featured')),
                ('featured_image', mezzanine.core.fields.FileField(max_length=1024, verbose_name='featured image', blank=True)),
                ('featured_image_header', mezzanine.core.fields.FileField(max_length=1024, verbose_name='featured image header', blank=True)),
                ('artists', models.ManyToManyField(related_name='metaevents', verbose_name='artists', to='festival.Artist', blank=True)),
                ('category', models.ForeignKey(related_name='festival_events', on_delete=django.db.models.deletion.SET_NULL, verbose_name='category', blank=True, to='festival.EventCategory', null=True)),
                ('event', models.ForeignKey(related_name='festival_events', on_delete=django.db.models.deletion.SET_NULL, verbose_name='festival event', blank=True, to='mezzanine_agenda.Event', null=True)),
            ],
            options={
                'db_table': 'festival_events',
                'verbose_name': 'festival event',
            },
        ),
        migrations.RemoveField(
            model_name='metaevent',
            name='artists',
        ),
        migrations.RemoveField(
            model_name='metaevent',
            name='category',
        ),
        migrations.RemoveField(
            model_name='metaevent',
            name='event',
        ),
        migrations.DeleteModel(
            name='MetaEvent',
        ),
    ]
