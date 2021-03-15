from django import forms

from orderapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, optype, wsgroup, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['min'] = 0


class OrderStatusForm(forms.Form):
    status_list = forms.ChoiceField(widget=forms.Select, choices=Order.ORDER_STATUS_CHOICES, label='Изменить статус заказа')

    def __init__(self, *args, **kwargs):
        super(OrderStatusForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
