import hashlib

from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from userapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from userapp.models import User


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
            user = form.save()
            params = {
                'user': user.id,
                'sendmail': 1,
            }
            if send_activation_code(user):
                print('Отправлено сообщение')
            else:
                params['sendmail'] = 0
                print('Что-то пошло не так!')
            return HttpResponseRedirect(reverse('user:verify') + build_GET(params))

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

    context = {
        'title': f'Профиль пользователя {request.user.username}',
        'form': form,
    }
    return render(request, 'userapp/profile.html', context=context)


def verify(request):
    if request.method == 'GET':
        user_id = int(request.GET['user'])
        try:
            user = User.objects.get(pk=user_id)
            print(user)
        except User.DoesNotExist:
            msg = 'Ошибка данных'
            error = True
        else:
            if 'sendmail' in request.GET:
                if request.GET['sendmail'] == '0':
                    msg = f'Не удалось отправить письмо на почту {user.email}. \
                            Повторите попытку позже.'
                    error = True
                else:
                    msg = f'На почту {user.email} отправлено письмо. \
                            Для активации учетной записи {user.username} перейдите по ссылке из письма'
                    error = False
            elif 'hash' in request.GET and request.GET['hash'] == get_sha1(user.email) \
                    and 'key' in request.GET and request.GET['key'] == user.activation_key \
                    and user.check_activation_key():
                user.is_active = True
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                msg = 'Активация успешно завершена! Теперь можете продолжить покупки.'
                error = False
            else:
                msg = 'Ошибка данных'
                error = True
    else:
        msg = 'Ошибка запроса'
        error = True

    context = {
        'msg': msg,
        'error': error
    }
    return render(request, 'userapp/verify.html', context=context)


def send_activation_code(user):
    args = {
        'user': user.pk,
        'hash': get_sha1(user.email),
        'key': user.activation_key,
    }
    link = settings.DOMAIN_NAME + reverse('userapp:verify') + build_GET(args)

    title = f"Подтверждение учетной записи {user.username}"
    message = f"Для подтверждения учетной записи {user.username} \
        на портале {settings.DOMAIN_NAME} перейдите по ссылке: \
        \n{link}"

    # print(title)
    # print(message)
    print(f"from: {settings.EMAIL_HOST_USER}, to: {user.email}")
    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def get_sha1(string):
    return hashlib.sha1(string.encode("utf8")).hexdigest()


def build_GET(args):
    return '?' + '&'.join([f'{str(v)}={str(args[v])}' for v in args]) if args else ''
