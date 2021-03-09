from django.urls import re_path

from orderapp.views import OrderList, OrderCreate
# import userapp.views as userapp


app_name = 'orderapp'

urlpatterns = [
    re_path(r'^$', OrderList.as_view(), name='order_list'),
    re_path(r'^create/$', OrderCreate.as_view(), name='order_create'),
]

