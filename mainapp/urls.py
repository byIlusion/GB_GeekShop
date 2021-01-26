from django.urls import path
import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('<int:cat_id>', mainapp.categories_product, name='category'),
]
