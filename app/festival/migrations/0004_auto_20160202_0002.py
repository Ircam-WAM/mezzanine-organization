# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0003_artist_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='content',
        ),
        migrations.AddField(
            model_name='artist',
            name='bio',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='bio', blank=True),
        ),
    ]
