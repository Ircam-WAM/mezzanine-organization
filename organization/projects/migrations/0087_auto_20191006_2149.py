# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-10-06 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization-projects', '0086_auto_20190527_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectresidencyarticle',
            name='credits',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='credits'),
        ),
        migrations.AddField(
            model_name='projectresidencyarticle',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='projectresidencyarticle',
            name='file',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default=None, null=True, upload_to='images', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='projectresidencyarticle',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectblock',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectblock',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcallblock',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcallblock',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcallfile',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcallimage',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcallimage',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectpageblock',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectpageblock',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectpageimage',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectpageimage',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectresidencyfile',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectresidencyimage',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectresidencyimage',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectresidencyuserimage',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectuserimage',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectworkpackage',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='title'),
        ),
    ]