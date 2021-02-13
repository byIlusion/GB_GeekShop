from django.urls import path
import adminapp.views as adminapp


app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    # Пользователи
    path('users/', adminapp.UsersListView.as_view(), name='users'),
    path('user-create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user-update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user-delete/<int:user_id>/', adminapp.user_delete, name='user_delete'),   # Оставил прежнюю реализацию
    # Категории
    path('categories/', adminapp.CategoryListView.as_view(), name='categories'),
    path('category-create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('category-update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/', adminapp.ProductListView.as_view(), name='products'),

    path('baskets/', adminapp.BasketListView.as_view(), name='baskets'),
]
