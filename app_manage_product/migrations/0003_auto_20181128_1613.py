# Generated by Django 2.1.3 on 2018-11-28 08:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_manage_product', '0002_auto_20181122_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_album',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 8, 13, 15, 58083, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='product_album',
            name='file_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product_album',
            name='file_type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_sell',
            field=models.DateField(default=datetime.datetime(2018, 11, 28, 8, 13, 15, 56709, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_update',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 8, 13, 15, 56742, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product_album',
            name='img',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='product_album',
            name='ordera',
            field=models.IntegerField(default=0),
        ),
    ]
