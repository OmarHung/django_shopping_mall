# Generated by Django 2.1.3 on 2018-11-22 03:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system_operation_record',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 22, 3, 36, 44, 734726, tzinfo=utc)),
        ),
    ]
