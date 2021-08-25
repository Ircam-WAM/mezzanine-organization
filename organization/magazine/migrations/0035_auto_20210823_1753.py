# Generated by Django 2.2.24 on 2021-08-23 15:53

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization-magazine', '0034_auto_20190703_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='articlepersonlistblockinline',
            name='person_list_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_person_list_block_inlines', to='organization-network.PersonListBlock', verbose_name='Person List Block'),
        ),
        migrations.AlterField(
            model_name='brief',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='local content'),
        ),
        migrations.AlterField(
            model_name='dynamiccontentarticle',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamiccontentmagazinecontent',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamicmultimediaarticle',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
    ]