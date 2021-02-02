from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from mainapp.models import Product
from basketapp.models import Basket


def basket_add(request, product_id=None):
    print(product_id)
    if product_id:
        product = Product.objects.filter(id=product_id)
        # product = get_object_or_404(Product, id=product_id)

        if product:
            print(len(product))
            print(product)
        # basket = Basket.objects.filter(user=request.user, product=product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, basket_id=None):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
