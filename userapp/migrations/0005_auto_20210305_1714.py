# Generated by Django 2.2.17 on 2021-03-05 10:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_auto_20210303_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 6, 10, 14, 36, 319638, tzinfo=utc), verbose_name='Время жизни ключа'),
        ),
    ]
