# Generated by Django 3.2.19 on 2023-06-01 12:50

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization_core', '0009_alter_metacategory_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metacategory',
            options={'ordering': ('_order',), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='metacategory',
            name='_order',
            field=mezzanine.core.fields.OrderField(null=True, verbose_name='Order'),
        ),
        migrations.AddField(
            model_name='metacategory',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='metacategory',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Logo'),
        ),
    ]