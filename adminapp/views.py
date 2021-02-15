from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from userapp.models import User
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket
from adminapp.forms import AdminUserCreate, AdminUserUpdate, AdminCategoryForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'Административная панель'}
    return render(request, 'adminapp/index.html', context)


class UsersListView(ListView):
    model = User
    template_name = 'adminapp/users.html'
    extra_context = {'title': 'Пользователи'}

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UsersListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/user_create.html'
    form_class = AdminUserCreate
    success_url = reverse_lazy('admin_staff:users')
    extra_context = {'title': 'Создать пользователя'}

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/user_update.html'
    form_class = AdminUserUpdate
    extra_context = {'title': 'Редактирование пользователя'}

    def get_success_url(self):
        self.success_url = reverse_lazy('admin_staff:user_update', args=[self.kwargs['pk']])
        return str(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_staff)
def user_delete(request, user_id=None):
    current_user = User.objects.get(id=user_id)
    current_user.is_active = not current_user.is_active
    current_user.save()
    return HttpResponseRedirect(reverse('admin_staff:user_update', args=[current_user.id]))


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    extra_context = {'title': 'Категории'}

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryListView, self).dispatch(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category.html'
    form_class = AdminCategoryForm
    success_url = reverse_lazy('admin_staff:categories')
    extra_context = {
        'title': 'Создать категорию',
        'action': reverse_lazy('adminapp:category_create'),
    }

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(request, *args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category.html'
    form_class = AdminCategoryForm
    success_url = reverse_lazy('admin_staff:categories')
    extra_context = {
        'title': 'Редактирование категории',
        'is_update': True,
    }

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context.update({
            'action': reverse_lazy('adminapp:category_update', args=[self.kwargs['pk']]),
        })
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category.html'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    extra_context = {'title': 'Товары'}

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListView, self).dispatch(request, *args, **kwargs)


class BasketListView(ListView):
    model = Basket
    template_name = 'adminapp/baskets.html'
    extra_context = {'title': 'Корзины пользователей'}

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(BasketListView, self).dispatch(request, *args, **kwargs)
