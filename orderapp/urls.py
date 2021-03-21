from django.urls import re_path

from orderapp.views import OrderList, OrderCreate, OrderDetail, OrderEdit, OrderDelete, order_forming_complete
# import userapp.views as userapp


app_name = 'orderapp'

urlpatterns = [
    re_path(r'^$', OrderList.as_view(), name='orders_list'),
    re_path(r'^create/$', OrderCreate.as_view(), name='order_create'),
    re_path(r'^detail/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    re_path(r'^edit/(?P<pk>\d+)/$', OrderEdit.as_view(), name='order_edit'),
    re_path(r'^delete/(?P<pk>\d+)/$', OrderDelete.as_view(), name='order_delete'),
    re_path(r'^forming/complete/(?P<pk>\d+)/$', order_forming_complete, name='order_forming_complete'),
]

