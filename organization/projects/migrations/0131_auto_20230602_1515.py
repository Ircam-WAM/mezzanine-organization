# Generated by Django 3.2.19 on 2023-06-02 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_projects', '0130_alter_project_meta_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcallimage',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcallimage',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcallimage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcollectionimage',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcollectionimage',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectcollectionimage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectpageimage',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectpageimage',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectpageimage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectresidencyimage',
            name='title',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectresidencyimage',
            name='title_en',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='projectresidencyimage',
            name='title_fr',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='title'),
        ),
    ]
