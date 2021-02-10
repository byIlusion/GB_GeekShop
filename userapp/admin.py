from django.contrib import admin
from userapp.models import User


# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_staff',
                    'is_superuser', 'is_active')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('-is_superuser', '-is_staff', '-is_active', 'username')
    fields = ('username', ('first_name', 'last_name'), 'email', ('is_active', 'is_staff', 'is_superuser'),
              'avatar', 'age', 'user_permissions', 'groups', 'password')
    readonly_fields = ('username', 'password')
