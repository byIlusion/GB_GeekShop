from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404

from mainapp.models import Product


class Order(models.Model):
    FORMING = "FM"
    SENT_TO_PROCEED = "STP"
    PROCEEDED = "PRD"
    PAID = "PD"
    READY = "RDY"
    CANCEL = "CNC"

    ORDER_STATUS_CHOICES = (
        (FORMING, "формируется"),
        (SENT_TO_PROCEED, "отправлен в обработку"),
        (PAID, "оплачен"),
        (PROCEEDED, "обрабатывается"),
        (READY, "готов к выдаче"),
        (CANCEL, "отменен"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Дата и время создания заказа', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата и время обновления заказа', auto_now=True)
    status = models.CharField(verbose_name='Статус заказа', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='Активен или удален заказ', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ ID {self.pk} (User {self.user.pk} - {self.user.username})'

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_total_cost(), items)))

    def get_products_quantity(self):
        items = self.orderitems.select_related()
        return len(items)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество заказанного товара', default=0)

    def __str__(self):
        return f'Заказ: {self.order.pk}, товар: {self.product.pk}, количество: {self.quantity}'

    @staticmethod
    def get_item(pk):
        return get_object_or_404(OrderItem, pk=pk)

    def get_total_cost(self):
        return self.product.price * self.quantity
