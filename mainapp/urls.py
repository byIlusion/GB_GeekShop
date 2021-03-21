# from django.urls import path
from django.urls import re_path
import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.products, name='index'),
    re_path(r'^(?P<category_id>\d+)/$', mainapp.products, name='products'),
    re_path(r'^info/(?P<product_id>\d+)/$', mainapp.product_info, name='product_info'),
]
