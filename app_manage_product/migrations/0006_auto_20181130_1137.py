# Generated by Django 2.1.3 on 2018-11-30 03:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_manage_product', '0005_auto_20181128_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_album',
            name='thumbnail_url',
        ),
        migrations.AlterField(
            model_name='product',
            name='date_sell',
            field=models.DateField(default=datetime.datetime(2018, 11, 30, 3, 37, 42, 526152, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_update',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 30, 3, 37, 42, 526214, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product_album',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 30, 3, 37, 42, 529083, tzinfo=utc)),
        ),
    ]
