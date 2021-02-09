from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test

from userapp.models import User
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket
from adminapp.forms import AdminUserCreate, AdminUserUpdate, AdminCategoryForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'Административная панель'}
    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda u: u.is_staff)
def users(request):
    context = {
        'title': 'Пользователи',
        'users': User.objects.all(),
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_staff)
def user_create(request):
    if request.method == 'POST':
        form = AdminUserCreate(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        form = AdminUserCreate()

    context = {
        'title': 'Создать пользователя',
        'form': form,
    }
    return render(request, 'adminapp/user_create.html', context)


@user_passes_test(lambda u: u.is_staff)
def user_update(request, user_id=None):
    current_user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = AdminUserUpdate(data=request.POST, files=request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[current_user.id]))
    else:
        form = AdminUserUpdate(instance=current_user)

    context = {
        'title': current_user.username,
        'form': form,
        'current_user': current_user,
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_staff)
def user_delete(request, user_id=None):
    current_user = User.objects.get(id=user_id)
    current_user.is_active = not current_user.is_active
    current_user.save()
    return HttpResponseRedirect(reverse('admin_staff:user_update', args=[current_user.id]))


@user_passes_test(lambda u: u.is_staff)
def categories(request):
    context = {
        'title': 'Категории',
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_staff)
def category_create(request):
    if request.method == 'POST':
        form = AdminCategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        form = AdminCategoryForm()

    context = {
        'title': 'Создать категорию',
        'form': form,
        'action': reverse('adminapp:category_create'),
        'is_update': False,
    }
    return render(request, 'adminapp/category.html', context)


@user_passes_test(lambda u: u.is_staff)
def category_update(request, category_id=None):
    current_category = ProductCategory.objects.get(id=category_id)
    if request.method == 'POST':
        form = AdminCategoryForm(data=request.POST, instance=current_category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        form = AdminCategoryForm(instance=current_category)

    context = {
        'title': 'Редактирование категории',
        'form': form,
        'action': reverse('adminapp:category_update', args=[current_category.id]),
        'is_update': True,
        'category': current_category,
    }
    return render(request, 'adminapp/category.html', context)


@user_passes_test(lambda u: u.is_staff)
def category_delete(request, category_id=None):
    current_category = ProductCategory.objects.get(id=category_id)
    current_category.delete()
    return HttpResponseRedirect(reverse('admin_staff:categories'))


@user_passes_test(lambda u: u.is_staff)
def products(request):
    context = {
        'title': 'Товары',
        'products': Product.objects.all(),
    }
    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_staff)
def baskets(request):
    context = {
        'title': 'Корзины пользователей',
        'baskets': Basket.get_all(),
    }
    return render(request, 'adminapp/baskets.html', context)
