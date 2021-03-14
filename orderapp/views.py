from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.dispatch import receiver

from orderapp.models import Order, OrderItem
from orderapp.forms import OrderItemForm
from basketapp.models import Basket


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket = Basket.get_items(user=self.request.user)
            if len(basket):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket[num].product
                    form.initial['quantity'] = basket[num].quantity
                    form.fields['quantity'].widget.attrs['max'] = basket[num].product.quantity + basket[num].quantity
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            """Очистку корзины перенес до сохранения заказа,
                т.к. нужно сначала переместить количество из корзины в остаток товара,
                а потом уже из остатка товара переместить в заказ.
                Иначе падает в ошибку, т.к. количество товара не может быть отрицательным.
            """
            Basket.get_items(user=self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderDetail(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


class OrderEdit(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy("order:orders_list")

    def get_context_data(self, **kwargs):
        data = super(OrderEdit, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            data["orderitems"] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data["orderitems"] = OrderFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # Delete empty order
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderEdit, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:orders_list')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('order:orders_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_with_save(instance, sender, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(pk=instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_with_delete(instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
