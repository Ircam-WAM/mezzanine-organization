# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-23 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('organization-magazine', '0003_articlepersonlistblockinline'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicContentArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('object_id', models.PositiveIntegerField(editable=False, null=True, verbose_name='related object')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization-magazine.Article', verbose_name='article')),
                ('content_type', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type')),
            ],
            options={
                'verbose_name': 'Dynamic Content Article',
                'ordering': ('_order',),
            },
        ),
    ]
