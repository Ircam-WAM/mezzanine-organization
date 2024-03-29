# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-28 14:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_magazine', '0014_brief_style'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleRelatedTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1024, null=True, verbose_name='title')),
                ('article', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_title', to='organization_magazine.Article', verbose_name='article')),
            ],
            options={
                'verbose_name': 'related title',
            },
        ),
        migrations.AlterOrderWithRespectTo(
            name='articlerelatedtitle',
            order_with_respect_to='article',
        ),
    ]
