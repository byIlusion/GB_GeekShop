from django import forms
import userapp.forms as userapp
from userapp.models import User
from mainapp.models import ProductCategory


class AdminUserCreate(userapp.UserRegisterForm):
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'password1', 'password2', 'age')

    def __init__(self, *args, **kwargs):
        super(AdminUserCreate, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'
        self.fields['avatar'].widget.attrs['placeholder'] = 'Аватар'


class AdminUserUpdate(userapp.UserEditForm):
    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'username', 'email', 'age')

    def __init__(self, *args, **kwargs):
        super(AdminUserUpdate, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = False


class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')
    
    def __init__(self, *args, **kwargs):
        super(AdminCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Описание категории'
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
