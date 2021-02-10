from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from userapp.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean_age(self):
        age = self.cleaned_data['age']
        if age > 100:
            raise forms.ValidationErrors('Вы слишком стары!')
        return age


class UserProfileForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'username', 'email', 'age')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['aria-describedby'] = 'usernameHelp'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['aria-describedby'] = 'emailHelp'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['age'].widget.attrs['aria-describedby'] = 'birthdayHelp'
        self.fields['age'].widget.attrs['type'] = 'date'
