# Generated by Django 3.2.19 on 2023-06-13 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_magazine', '0053_auto_20230602_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='topics',
        ),
    ]