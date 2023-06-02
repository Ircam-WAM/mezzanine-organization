# Generated by Django 3.2.19 on 2023-05-23 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_core', '0007_auto_20230418_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='metacategory',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='metacategory',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='metacategory',
            name='name_en',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='metacategory',
            name='name_fr',
            field=models.CharField(max_length=512, null=True, verbose_name='name'),
        ),
    ]