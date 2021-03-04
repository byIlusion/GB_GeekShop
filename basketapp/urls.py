from django.urls import re_path
import basketapp.views as basketapp


app_name = 'basketapp'

urlpatterns = [
    re_path(r'^add/(?P<product_id>\d+)/$', basketapp.basket_add, name='basket_add'),
    re_path(r'^remove/(?P<basket_id>\d+)/$', basketapp.basket_remove, name='basket_remove'),
    re_path(r'^edit/(?P<basket_id>\d+)/(?P<quantity>\d+)/$', basketapp.basket_edit, name='basket_edit'),
]

