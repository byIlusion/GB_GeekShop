# Generated by Django 2.2.19 on 2021-03-21 17:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_auto_20210316_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 22, 17, 2, 22, 179930, tzinfo=utc), verbose_name='Время жизни ключа'),
        ),
    ]
