# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0002_auto_20160224_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'event category',
            },
        ),
        migrations.CreateModel(
            name='PageCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'page category',
            },
        ),
        migrations.RemoveField(
            model_name='artist',
            name='content',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='content_en',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='content_fr',
        ),
        migrations.AddField(
            model_name='artist',
            name='bio',
            field=mezzanine.core.fields.RichTextField(verbose_name='biography', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='bio_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='biography', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='bio_fr',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='biography', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='description_en',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='description_fr',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(max_length=512, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='metaevent',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='featured'),
        ),
        migrations.AddField(
            model_name='metaevent',
            name='category',
            field=models.ForeignKey(related_name='meta_events', on_delete=django.db.models.deletion.SET_NULL, verbose_name='category', blank=True, to='festival.EventCategory', null=True),
        ),
    ]
