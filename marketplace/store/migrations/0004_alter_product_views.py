# Generated by Django 3.2.2 on 2021-06-27 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
