from django.shortcuts import render
import json


def main(request):
    context = {
        'title': 'GeekShop. главная',
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request):
    context = {
        'title': 'GeekShop. каталог',
        'products': None,
        'path_imgs': 'vendor/img/products/',
        'menu_catalog': None,
    }

    try:
        with open("mainapp/fixtures/products.json", 'r') as f:
            context['products'] = json.loads(f.read())
    except IOError:
        print("Ошибка чтения!")

    try:
        with open("mainapp/fixtures/menu_catalog.json", 'r') as f:
            context['menu_catalog'] = json.loads(f.read())
    except IOError:
        print("Ошибка чтения!")

    return render(request, 'mainapp/products.html', context=context)
