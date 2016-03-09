# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mezzanine_agenda', '0002_auto_20160224_1142'),
        ('festival', '0006_auto_20160303_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='festivalevent',
            name='artists',
        ),
        migrations.RemoveField(
            model_name='festivalevent',
            name='category',
        ),
        migrations.RemoveField(
            model_name='festivalevent',
            name='event',
        ),
        migrations.AddField(
            model_name='artist',
            name='events',
            field=models.ManyToManyField(related_name='artists', verbose_name='events', to='mezzanine_agenda.Event', blank=True),
        ),
        migrations.DeleteModel(
            name='EventCategory',
        ),
        migrations.DeleteModel(
            name='FestivalEvent',
        ),
    ]
