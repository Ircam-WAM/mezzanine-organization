# Generated by Django 3.2.19 on 2023-06-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0056_home_punchline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeimage',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='homeimage',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='homeimage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='pageimage',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='pageimage',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='pageimage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
    ]
