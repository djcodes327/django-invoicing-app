from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = (
        ('Personal Details', {
            'fields': (('username', 'email'), ('first_name', 'last_name'), ('password',)),
        }),
        ('Contact Information', {
            'fields': (('address', 'city', 'state'), ('country', 'postal_code')),
        }),
        ('About Me and Birth Date', {
            'fields': (('role', 'company',),)
        }),
        ('Company Information', {
            'fields': ('about_me', 'date_of_birth')
        }),
        ('Website and Pictures', {
            'fields': ('website', 'profile_pic', 'cover_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff',
                'is_superuser')
        }),
    )
    readonly_fields = ['last_login', 'date_joined']


admin.site.register(CustomUser, UserAdmin)
