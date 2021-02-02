from django.shortcuts import render, HttpResponseRedirect

from mainapp.models import Product
from basketapp.models import Basket


def basket_add(request, product_id=None):
    if product_id:
        product = Product.objects.filter(id=product_id)
        if product.exists():
            product = product.first()
            basket = Basket.objects.filter(user=request.user, product=product)
            basket = basket.first() if basket.exists() else Basket(user=request.user, product=product)
            basket.quantity += 1
            if basket.quantity > product.quantity:
                basket.quantity = product.quantity
            basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, basket_id=None):
    if basket_id:
        basket = Basket.objects.filter(id=basket_id)
        if basket.exists():
            basket.first().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
