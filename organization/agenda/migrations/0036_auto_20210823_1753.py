# Generated by Django 2.2.24 on 2021-08-23 15:53

from django.db import migrations, models
import django.db.models.deletion
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organization-agenda', '0035_auto_20210628_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontentevent',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='dynamicmultimediaevent',
            name='content_type',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='eventimage',
            name='file',
            field=mezzanine.core.fields.FileField(max_length=1024, upload_to='images', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='eventlink',
            name='link_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization-core.LinkType', verbose_name='link type'),
        ),
        migrations.AlterField(
            model_name='eventpersonlistblockinline',
            name='person_list_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='organization-network.PersonListBlock', verbose_name='Person List Block'),
        ),
    ]
