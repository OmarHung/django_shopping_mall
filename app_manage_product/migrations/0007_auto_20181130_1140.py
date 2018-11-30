# Generated by Django 2.1.3 on 2018-11-30 03:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_manage_product', '0006_auto_20181130_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_album',
            name='ori_name',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_sell',
            field=models.DateField(default=datetime.datetime(2018, 11, 30, 3, 40, 26, 258871, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_update',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 30, 3, 40, 26, 258934, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product_album',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 30, 3, 40, 26, 261040, tzinfo=utc)),
        ),
    ]