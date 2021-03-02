from django.urls import re_path
import adminapp.views as adminapp


app_name = 'adminapp'

urlpatterns = [
    re_path(r'^$', adminapp.index, name='index'),
    # Пользователи
    re_path(r'^users/$', adminapp.UsersListView.as_view(), name='users'),
    re_path(r'^user-create/$', adminapp.UserCreateView.as_view(), name='user_create'),
    re_path(r'^user-update/(?P<pk>\d+)/$', adminapp.UserUpdateView.as_view(), name='user_update'),
    re_path(r'^user-delete/(?P<user_id>\d+)/$', adminapp.user_delete, name='user_delete'),   # Оставил прежнюю реализацию
    # Категории
    re_path(r'^categories/$', adminapp.CategoryListView.as_view(), name='categories'),
    re_path(r'^category-create/$', adminapp.CategoryCreateView.as_view(), name='category_create'),
    re_path(r'^category-update/(?P<pk>\d+)/$', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    re_path(r'^category-delete/(?P<pk>\d+)/$', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    re_path(r'^products/$', adminapp.ProductListView.as_view(), name='products'),

    re_path(r'^baskets/$', adminapp.BasketListView.as_view(), name='baskets'),
]
