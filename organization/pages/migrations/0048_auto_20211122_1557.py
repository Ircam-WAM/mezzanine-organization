# Generated by Django 3.2.8 on 2021-11-22 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_pages', '0047_auto_20210823_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagerelatedtitle',
            name='in_navbar',
            field=models.BooleanField(default=False, verbose_name='in navbar ?'),
        ),
        migrations.AlterField(
            model_name='custompage',
            name='separator',
            field=models.CharField(default='0,0,1,1,1,1', max_length=32, verbose_name='\n        separator before blocks,\n        0 : no sepeartor\n        1 : separator\n\n        order of blocks (\n            0: images,\n            1: multimedias,\n            2: liste de personnes,\n            3: blocks,\n            4: listes des produits,\n            5: Dynamic Content pages\n        )\n\n        '),
        ),
    ]
