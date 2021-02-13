from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import UpdateView

from userapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from userapp.models import User
from basketapp.models import Basket


@user_passes_test(lambda u: u.is_anonymous, login_url='user:profile', redirect_field_name='')
def login(request):
    form = UserLoginForm(data=request.POST or None)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))
    context = {
        'title': 'GeekShop - Авторизация',
        'form': form,
        'next': next,
    }
    return render(request, 'userapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@user_passes_test(lambda u: u.is_anonymous, login_url='user:profile', redirect_field_name='')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegisterForm()

    # Тут реализовал раскладывание по 2 в группу чтоб потом было проще отрендерить форму
    list_form = [f for f in form]
    grouped_form = [list_form[i*2:i*2+2] for i in range(len(list_form) // 2 + len(list_form) % 2)]
    context = {
        'title': 'GeekShop - Регистрация',
        'form': form,
        'grouped_form': grouped_form
    }
    return render(request, 'userapp/register.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    basket = Basket.objects.filter(user=request.user)
    context = {
        'title': f'Профиль пользователя {request.user.username}',
        'form': form,
        'basket': basket,
        # 'basket_statistic': Basket.basket_totals(basket),
    }
    return render(request, 'userapp/profile.html', context=context)
