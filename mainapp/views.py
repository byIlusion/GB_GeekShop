from django.shortcuts import render, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from mainapp.models import ProductCategory, Product


def main(request):
    context = {
        'title': 'GeekShop. главная',
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, category_id=None):
    if category_id is not None:
        product_list = Product.objects.filter(category_id=category_id)
    else:
        product_list = Product.objects.all()

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
        'categories': ProductCategory.objects.all(),
        'category_id': category_id,
    }
    return render(request, 'mainapp/products.html', context=context)
