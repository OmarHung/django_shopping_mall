# Generated by Django 2.1.3 on 2018-11-30 03:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_manage_admin_user', '0005_auto_20181128_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_user',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 30, 3, 37, 42, 530877, tzinfo=utc)),
        ),
    ]
