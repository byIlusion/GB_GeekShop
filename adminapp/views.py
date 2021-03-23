from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
# from django.forms import inlineformset_factory
from django import forms
from django.db import transaction

from userapp.models import User
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket
from adminapp.forms import AdminUserCreate, AdminUserUpdate, AdminCategoryForm
from orderapp.models import Order, OrderItem
from orderapp.forms import OrderItemForm, OrderStatusForm


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
    if user_id is not None:
        user_id = int(user_id)
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


class OrdersList(ListView):
    model = Order
    template_name = 'adminapp/orders_list.html'
    extra_context = {'title': 'Заказы'}

    def get_queryset(self):
        return Order.objects.filter(is_active=True)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    template_name = 'adminapp/order_update.html'

    def get_success_url(self):
        self.success_url = reverse_lazy('admin_staff:order_update', args=[self.kwargs['pk']])
        return str(self.success_url)

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = forms.inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0)
        data['status_list'] = OrderStatusForm
        data['status_list'].base_fields['status_list'].initial = data['object'].status
        if self.request.POST:
            data["orderitems"] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data["orderitems"] = OrderFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.request.POST and 'status_list' in self.request.POST:
                self.object.status = self.request.POST['status_list']
                self.object.save()

        # Delete empty order
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderUpdate, self).form_valid(form)
