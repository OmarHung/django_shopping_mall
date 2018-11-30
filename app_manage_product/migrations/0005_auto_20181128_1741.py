# Generated by Django 2.1.3 on 2018-11-28 09:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_manage_product', '0004_auto_20181128_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_sell',
            field=models.DateField(default=datetime.datetime(2018, 11, 28, 9, 41, 5, 23970, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_update',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 9, 41, 5, 24037, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product_album',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 28, 9, 41, 5, 28556, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product_album',
            name='name',
            field=models.CharField(max_length=60, null=True),
        ),
    ]