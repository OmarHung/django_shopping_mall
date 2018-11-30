# Generated by Django 2.1.3 on 2018-11-08 08:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('ori_price', models.IntegerField(default=0)),
                ('sale_price', models.IntegerField(default=0)),
                ('date_sell', models.DateField(default=datetime.datetime(2018, 11, 8, 8, 10, 7, 861880, tzinfo=utc))),
                ('date_update', models.DateTimeField(default=datetime.datetime(2018, 11, 8, 8, 10, 7, 861944, tzinfo=utc))),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Product_spec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('spec_1', models.CharField(max_length=10)),
                ('spec_2', models.CharField(max_length=10)),
                ('stock', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'product_spec',
            },
        ),
    ]