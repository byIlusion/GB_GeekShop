from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import F

from mainapp.models import Product
from basketapp.models import Basket


@login_required
def basket_add(request, product_id=None):
    # if 'login' in request.META.get('HTTP_REFERER'):
    #     return HttpResponseRedirect(reverse('mainapp:index'))

    if product_id:
        product_id = int(product_id)
        product = get_object_or_404(Product, id=product_id)
        basket = Basket.objects.filter(user=request.user, product=product).first()

        if product.quantity > 0:
            if not basket:
                basket = Basket(user=request.user, product=product)
                basket.quantity += 1
            else:
                basket.quantity = F('quantity') + 1

        basket.save()

        # update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        # print(f'query basket_add: {update_queries}')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
