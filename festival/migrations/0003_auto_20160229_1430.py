# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0002_auto_20160225_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='photo_description',
            field=models.TextField(verbose_name='photo description', blank=True),
        ),
        migrations.AddField(
            model_name='festivalevent',
            name='featured_image_description',
            field=models.TextField(verbose_name='featured image description', blank=True),
        ),
    ]
