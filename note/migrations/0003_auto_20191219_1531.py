# Generated by Django 2.2 on 2019-12-19 10:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0002_auto_20191219_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 12, 19, 15, 31, 6, 56769), null=True),
        ),
        migrations.AlterField(
            model_name='notes',
            name='reminder',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 12, 19, 15, 31, 6, 56825), null=True),
        ),
    ]
