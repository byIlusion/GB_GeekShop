from django.shortcuts import render
from mainapp.models import ProductCategory, Product
import json


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

    # Если в базе нет категорий, то загружаем из JSON и сохраняем в БД
    if len(context['categories']) == 0:
        try:
            with open('mainapp/fixtures/menu_catalog.json', 'r') as f:
                categories = json.loads(f.read())
                for category in categories:
                    ProductCategory.objects.create(name=category['name'], description=category['description'])
                context['categories'] = ProductCategory.objects.all()
        except IOError:
            print('Ошибка чтения!')

    # Если в базе нет товаров, то загружаем из JSON и сохраняем в БД
    if len(context['products']) == 0:
        try:
            with open('mainapp/fixtures/products.json', 'r') as f:
                products = json.loads(f.read())
                for product in products:
                    prod = Product()
                    prod.name = product['name']
                    prod.short_description = product['short_description']
                    prod.description = product['description']
                    prod.category = ProductCategory.objects.get(name=product['category'])
                    prod.price = product['price']
                    prod.quantity = product['quantity']
                    # Картинки уже загружены через админку, поэтому просто добавляются пути до них
                    prod.image = 'products_images/' + product['image']
                    prod.save()
                context['products'] = Product.objects.all()
        except IOError:
            print('Ошибка чтения!')

    return render(request, 'mainapp/products.html', context=context)


def categories_product(request, cat_id=None):
    context = {
        'title': 'GeekShop. каталог',
        'products': Product.objects.filter(category=cat_id),
        'categories': ProductCategory.objects.all(),
        'cat_id': cat_id,
    }

    return render(request, 'mainapp/products.html', context=context)
