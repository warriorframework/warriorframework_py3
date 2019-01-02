# -*- coding: utf-8 -*-


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django.contrib import admin
from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm):
        model = User
        fields = BaseUserCreationForm.Meta.fields + ('expires',)


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm):
        model = User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    model = User
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = BaseUserAdmin.list_display + ('expires',)
    list_filter = BaseUserAdmin.list_filter + ('expires',)
    fieldsets = (
        ('None', {'fields': (
            'username',
            'password',
        )}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'email',
        )}),
        ('Permissions', {'fields': (
            'expires',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        ('Important dates', {'fields': (
            'last_login',
            'date_joined',
        )}),
    )
    limited_fieldsets = (
        (None, {'fields': (
            'username',
        )}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'email',
        )}),
        ('Important dates', {'fields': (
            'last_login',
            'date_joined',
        )}),
    )


admin.site.register(User, UserAdmin)
