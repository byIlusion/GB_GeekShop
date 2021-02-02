# Generated by Django 2.2.17 on 2021-01-26 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название категории')),
                ('description', models.TextField(blank=True, verbose_name='Описание категории')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Наименование товара')),
                ('short_description', models.CharField(max_length=256, verbose_name='Краткое описание товара')),
                ('description', models.TextField(blank=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Стоимость')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество товара')),
                ('image', models.ImageField(blank=True, upload_to='products_images', verbose_name='Путь до изображения товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProductCategory', verbose_name='ID категории')),
            ],
        ),
    ]