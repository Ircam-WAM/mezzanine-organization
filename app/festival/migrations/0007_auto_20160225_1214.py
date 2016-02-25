# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0006_auto_20160225_0503'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='content',
            field=mezzanine.core.fields.RichTextField(default='', verbose_name='Content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='description_fr',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='title_en',
            field=models.CharField(max_length=500, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='video',
            name='title_fr',
            field=models.CharField(max_length=500, null=True, verbose_name='Title'),
        ),
    ]
