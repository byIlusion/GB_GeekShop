from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse

from mainapp.models import Product
from basketapp.models import Basket


@login_required
def basket_add(request, product_id=None):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('mainapp:index'))

    if product_id:
        product_id = int(product_id)
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
    # return JsonResponse({'result': 'added'})


@login_required
def basket_remove(request, basket_id=None):
    if basket_id:
        basket_id = int(basket_id)
        basket = Basket.objects.filter(id=basket_id)
        if basket.exists():
            basket.first().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, basket_id, quantity):
    if request.is_ajax():
        basket_id = int(basket_id)
        quantity = int(quantity)
        basket = Basket.objects.filter(id=basket_id)
        if basket.exists():
            item = basket.first()
            if quantity == 0:
                item.delete()
            else:
                if quantity - Basket.get_item(item.pk).quantity <= item.product.quantity:
                    item.quantity = quantity
                else:
                    item.quantity += item.product.quantity
                item.save()
        context = {
            'basket': Basket.objects.filter(user=request.user)
        }
        result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})
