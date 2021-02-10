from django.urls import path
import adminapp.views as adminapp


app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    # Пользователи
    path('users/', adminapp.users, name='users'),
    path('user-update/<int:user_id>/', adminapp.user_update, name='user_update'),
    path('user-create/', adminapp.user_create, name='user_create'),
    path('user-delete/<int:user_id>/', adminapp.user_delete, name='user_delete'),
    # Категории
    path('categories/', adminapp.categories, name='categories'),
    path('category-update/<int:category_id>/', adminapp.category_update, name='category_update'),
    path('category-create/', adminapp.category_create, name='category_create'),
    path('category-delete/<int:category_id>/', adminapp.category_delete, name='category_delete'),

    path('products/', adminapp.products, name='products'),

    path('baskets/', adminapp.baskets, name='baskets'),
]
