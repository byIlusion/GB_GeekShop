from django.db import models
from userapp.models import User
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name='ID пользователя', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='ID товара', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество товара в корзине', default=0)
    create_timestamp = models.DateTimeField(verbose_name='Дата и время добавления товара в корзину', auto_now_add=True)

    def __str__(self):
        return f'{self.id}: Корзина пользователя {self.user.username} | Товар: {self.product.name} ({self.quantity} шт.)'

    def sum(self):
        return self.quantity * self.product.price

    @staticmethod
    def stat(basket):
        result = {
            'count_all': 0,
            'sum_all': 0.0,
        }
        for item in basket:
            result['count_all'] += item.quantity
            result['sum_all'] += float(item.sum())
        return result

    @staticmethod
    def stat_by_user(user):
        basket = Basket.objects.filter(user=user)
        return Basket.stat(basket)
