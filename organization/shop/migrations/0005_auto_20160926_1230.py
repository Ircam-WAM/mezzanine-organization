# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-26 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20160907_1726'),
        ('pages', '0005_auto_20160923_1219'),
        ('organization_shop', '0004_auto_20160926_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageProductList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'product list',
                'verbose_name_plural': 'product lists',
            },
        ),
        migrations.CreateModel(
            name='ProductListProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('_order',),
            },
        ),
        migrations.RenameModel(
            old_name='ProductBlock',
            new_name='ProductList',
        ),
        migrations.RemoveField(
            model_name='pageproductblock',
            name='page',
        ),
        migrations.RemoveField(
            model_name='pageproductblock',
            name='product_block',
        ),
        migrations.RemoveField(
            model_name='productblockproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productblockproduct',
            name='product_block',
        ),
        migrations.AlterModelOptions(
            name='productlist',
            options={'verbose_name': 'product list', 'verbose_name_plural': 'product lists'},
        ),
        migrations.DeleteModel(
            name='PageProductBlock',
        ),
        migrations.DeleteModel(
            name='ProductBlockProduct',
        ),
        migrations.AddField(
            model_name='productlistproduct',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='organization_shop.ProductList', verbose_name='product list'),
        ),
        migrations.AddField(
            model_name='productlistproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lists', to='shop.Product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='pageproductlist',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='organization_shop.ProductList', verbose_name='product list'),
        ),
        migrations.AddField(
            model_name='pageproductlist',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_lists', to='pages.Page', verbose_name='page'),
        ),
    ]
