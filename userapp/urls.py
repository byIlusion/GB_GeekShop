from django.urls import re_path
import userapp.views as userapp


app_name = 'userapp'

urlpatterns = [
    re_path(r'^login/$', userapp.login, name='login'),
    re_path(r'^logout/$', userapp.logout, name='logout'),
    re_path(r'^register/$', userapp.register, name='register'),
    re_path(r'^profile/$', userapp.profile, name='profile'),
    re_path(r'^verify/$', userapp.verify, name='verify'),
]

