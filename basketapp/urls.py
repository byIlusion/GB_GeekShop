from django.urls import path
import basketapp.views as basketapp


app_name = 'basketapp'

urlpatterns = [
    path('add/<int:product_id>', basketapp.basket_add, name='basket_add'),
    path('remove/<int:basket_id>', basketapp.basket_remove, name='basket_remove'),
]

