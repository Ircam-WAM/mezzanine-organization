# Generated by Django 3.2.8 on 2021-12-02 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0152_auto_20211125_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentpage',
            name='displayed_in_navbars',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='teampage',
            name='displayed_in_navbars',
            field=models.BooleanField(default=True),
        ),
    ]