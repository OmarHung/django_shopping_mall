# Generated by Django 2.1.3 on 2018-12-10 08:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_manage_admin_user', '0009_auto_20181210_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_user',
            name='date_add',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 10, 8, 20, 37, 685778, tzinfo=utc)),
        ),
    ]
