# Generated by Django 3.2.19 on 2023-06-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_core', '0013_alter_metacategory_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='metacategory',
            name='icon_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='icon id'),
        ),
    ]