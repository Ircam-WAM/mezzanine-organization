# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0003_auto_20160229_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='photo_alignment',
            field=models.CharField(default=b'left', max_length=32, verbose_name='photo alignment', choices=[(b'left', 'left'), (b'right', 'right')]),
        ),
        migrations.AddField(
            model_name='artist',
            name='photo_featured',
            field=mezzanine.core.fields.FileField(max_length=1024, verbose_name='photo featured', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='photo_featured_credits',
            field=models.CharField(max_length=255, null=True, verbose_name='photo featured credits', blank=True),
        ),
    ]
