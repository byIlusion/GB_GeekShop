# Generated by Django 2.2.19 on 2021-03-16 13:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0008_auto_20210309_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 17, 13, 27, 43, 623880, tzinfo=utc), verbose_name='Время жизни ключа'),
        ),
    ]