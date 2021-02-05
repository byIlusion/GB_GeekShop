from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from userapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm

from basketapp.models import Basket


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'GeekShop - Авторизация',
        'form': form,
    }
    return render(request, 'userapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
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


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
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
        'basket_statistic': Basket.stat(basket),
    }
    return render(request, 'userapp/profile.html', context=context)
