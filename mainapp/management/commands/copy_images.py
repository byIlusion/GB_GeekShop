from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
from mainapp.models import Product

import os
import shutil


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        copied = []
        uncopied = []
        if not os.path.exists(settings.MEDIA_ROOT):
            os.mkdir(settings.MEDIA_ROOT)
        try:
            for product in products:
                path_media = os.path.join(settings.MEDIA_ROOT, str(product.image))
                if not os.path.exists(path_media):
                    print(f'Файл не найден: {path_media}')
                    image = str(product.image).split('/')
                    image = os.path.join('vendor/img/products', image[len(image) - 1])
                    path_static = FileSystemFinder().find(image)
                    if path_static:
                        shutil.copy(path_static, path_media)
                        print(f'{image} - Файл скопирован')
                        copied.append(image)
                    else:
                        uncopied.append(image)
        except FileNotFoundError:
            print(f'Не создана конечная папка')
        print(f'Скопировано изображений: {len(copied)}')
        if uncopied:
            delimeter = '\n'
            print(f'Не найденные изображения:\n{delimeter.join(uncopied)}')
