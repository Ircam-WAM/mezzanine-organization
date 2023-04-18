# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-30 10:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('organization_magazine', '0022_auto_20181102_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicMultimediaArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('object_id', models.PositiveIntegerField(editable=False, null=True, verbose_name='related object')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_multimedia', to='organization_magazine.Article', verbose_name='article')),
                ('content_type', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type')),
            ],
            options={
                'verbose_name': 'Multimedia',
                'ordering': ('_order',),
            },
        ),
    ]
