from django.shortcuts import render
from mainapp.models import ProductCategory, Product


def main(request):
    context = {
        'title': 'GeekShop. главная',
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request):
    context = {
        'title': 'GeekShop. каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/products.html', context=context)


def categories_product(request, cat_id=None):
    context = {
        'title': 'GeekShop. каталог',
        'products': Product.objects.filter(category=cat_id),
        'categories': ProductCategory.objects.all(),
        'cat_id': cat_id,
    }
    return render(request, 'mainapp/products.html', context=context)
