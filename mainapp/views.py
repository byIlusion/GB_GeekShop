from django.shortcuts import render, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.cache import cache
# from django.views.decorators.cache import cache_page

from mainapp.models import ProductCategory, Product


class Fact(object):
    def get_factorial(self):
        fact = 1
        for i in range(1, 15000 + 1):
            fact = fact * i
        return fact


# @cache_page(600)
def main(request):
    context = {
        'title': 'GeekShop. главная',
        "fact": Fact()
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, category_id=None):
    if category_id is not None:
        category_id = int(category_id)
        key = f'products_{category_id}'
    else:
        key = 'products'
    product_list = cache.get(key)
    if product_list is None:
        product_list = Product.get_items(category_id=category_id)
        cache.set(key, product_list)

    per_page = 3
    if 'page' in request.GET and int(request.GET['page']) == 1:
        if category_id:
            return HttpResponseRedirect(reverse('mainapp:products', args=[category_id]))
        else:
            return HttpResponseRedirect(reverse('mainapp:index'))
    page = int(request.GET['page']) if 'page' in request.GET and int(request.GET['page']) >= 1 else 1
    paginator = Paginator(object_list=product_list, per_page=per_page)
    product_paginator = paginator.page(page)
    context = {
        'title': 'GeekShop. каталог',
        'products': product_paginator,
        'categories': get_categories(),
        'category_id': category_id,
    }
    return render(request, 'mainapp/products.html', context=context)


def get_categories():
    key = 'categories'
    categories = cache.get(key)
    if categories is None:
        categories = ProductCategory.objects.all()
        cache.set(key, categories)
    return categories


def product_info(request, product_id):
    if request.is_ajax():
        product_id = int(product_id)
        key = f'product_{product_id}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=product_id)
            cache.set(key, product)
        # print(product.image)
        result = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'short_description': product.short_description,
            'category_id': product.category.id,
            'category_name': product.category.name,
            'price': product.price,
            'quantity': product.quantity,
            'image': str(product.image),
        }
        return JsonResponse(result)
