from django.views.generic import ListView, CreateView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.db import transaction

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
    success_url = reverse_lazy('order:order_list')

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket = Basket.objects.filter(user=self.request.user)
            print(len(basket))
            print(basket)
            if len(basket):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket))
                formset = OrderFormSet()
                print(formset)
                for num, form in enumerate(formset.forms):
                    form.initial["product"] = basket[num].product
                    form.initial["quantity"] = basket[num].quantity
            else:
                formset = OrderFormSet()

        data["orderitems"] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            Basket.objects.filter(user=self.request.user).delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)
