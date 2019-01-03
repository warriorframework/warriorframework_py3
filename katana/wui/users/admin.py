# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User


class UserCreationForm(BaseUserCreationForm):
    # Modify User Creation Form according to
    # https://django-authtools.readthedocs.io/en/latest/how-to/invitation-email.html
    # Set passwords to not required in order to integrate with LDAP passwords

    def __init__(self, *args, **kwargs):
        super(BaseUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

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
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
        ('Password', {
            'description': "Optionally, set user's password here.\n" +
                           "Leave fields blank if user password will be verified " +
                           "through 3rd party authentication such as LDAP or SAML SSO.",
            'fields': ('password1', 'password2',),
            'classes': ('wide',),
        }),
        ('Expiry', {
            'description': "Optionally, set user's expiry date here",
            'fields': ('expires',),
            'classes': ('wide',),
        }),
    )

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

    def save_model(self, request, obj, form, change):
        # Set user password unusable if password fields are left blank
        if not change and not form.cleaned_data['password1'] and not form.cleaned_data['password2']:
            obj.set_unusable_password()
        obj.save()


admin.site.register(User, UserAdmin)
