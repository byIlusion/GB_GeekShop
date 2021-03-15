from django.db import models
from django.shortcuts import get_object_or_404
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

    @property
    def total_quantity(self):
        basket = Basket.get_items(user=self.user)
        return Basket.basket_total_quantity(basket)

    @property
    def total_sum(self):
        basket = Basket.get_items(user=self.user)
        return Basket.basket_total_sum(basket)

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_item(pk):
        return get_object_or_404(Basket, pk=pk)

    @staticmethod
    def basket_total_quantity(basket):
        """Статичный метод для подсчета общего количества всех товаров запрашиваемой корзины

        :param basket: Товары корзины (список)
        :return: Общее количество всех товаров
        """
        return sum(item.quantity for item in basket)

    @staticmethod
    def basket_total_sum(basket):
        """Статичный метод для суммирования стоимости всех товаров в запрашиваемой корзине

        :param basket: Товары корзины (список)
        :return: Сумма всех товаров
        """
        return sum(item.sum() for item in basket)

    @staticmethod
    def basket_totals(basket):
        """Статичный метод для сбора статистики по запрашиваемой корзине
        Позволяет собрать статистику не прибегая к повторной загрузки товаров корзины из БД

        :param basket: Товары корзины (список)
        :return: Словарь с Общим количество товаров и суммой всех этих товаров
        """
        return {
            'total_quantity': Basket.basket_total_quantity(basket),
            'total_sum': Basket.basket_total_sum(basket),
        }

    @staticmethod
    def basket_totals_by_user(user):
        """Статичный метод для сбора статистики по корзине для запрашиваемого пользователя

        :param user: Объект пользователя
        :return: Словарь с Общим количество товаров и суммой всех этих товаров
        """
        basket = Basket.get_items(user=user)
        return Basket.basket_totals(basket)

    @staticmethod
    def get_all():
        return Basket.objects.all().order_by('-id')
