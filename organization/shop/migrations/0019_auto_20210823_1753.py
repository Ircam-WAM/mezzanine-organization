# Generated by Django 2.2.24 on 2021-08-23 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization-shop', '0018_auto_20191107_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productexternalshop',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_external_shop', to='shop.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='productexternalshop',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_external_shop', to='mezzanine_agenda.ExternalShop', verbose_name='shop'),
        ),
        migrations.AlterField(
            model_name='productlink',
            name='link_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization-core.LinkType', verbose_name='link type'),
        ),
        migrations.AlterField(
            model_name='teamproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team', to='shop.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='teamproduct',
            name='teams',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='organization-network.Team', verbose_name='team'),
        ),
    ]
