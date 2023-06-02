# Generated by Django 3.2.18 on 2023-04-25 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_network', '0156_merge_0115_auto_20230424_1520_0155_auto_20230424_1857'),
        ('organization_magazine', '0041_alter_article_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='department',
            field=models.ForeignKey(blank=True, limit_choices_to={'id__in': ()}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='organization_network.department', verbose_name='department'),
        ),
    ]