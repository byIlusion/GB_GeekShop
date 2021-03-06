from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=64, unique=True)
    description = models.TextField(verbose_name='Описание категории', blank=True)
    is_active = models.BooleanField(verbose_name='Активность категории', default=True)

    def __str__(self):
        return f'{self.name} ({self.id})'


class Product(models.Model):
    name = models.CharField(verbose_name='Наименование товара', max_length=128)
    short_description = models.CharField(verbose_name='Краткое описание товара', max_length=256)
    description = models.TextField(verbose_name='Описание товара', blank=True)
    category = models.ForeignKey(ProductCategory, verbose_name='ID категории', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Количество товара', default=0, db_index=True)
    image = models.ImageField(verbose_name='Путь до изображения товара', upload_to='products_images', blank=True)
    is_active = models.BooleanField(verbose_name='Активность товара', default=True)
    
    def __str__(self):
        return f'{self.id}: {self.name} ({self.category.name})'

    @staticmethod
    def get_items(category_id=None):
        if category_id is not None:
            return Product.objects.filter(quantity__gt=0, category_id=category_id, is_active=True).order_by('id')
        else:
            return Product.objects.filter(quantity__gt=0, is_active=True).order_by('id')
