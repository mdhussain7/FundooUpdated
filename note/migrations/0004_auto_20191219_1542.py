# Generated by Django 2.2 on 2019-12-19 10:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_auto_20191219_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='created_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 12, 19, 15, 42, 32, 721499), null=True),
        ),
        migrations.AlterField(
            model_name='notes',
            name='reminder',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 12, 19, 10, 12, 32, 721573, tzinfo=utc), null=True),
        ),
    ]