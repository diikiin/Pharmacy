from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User


@admin.register(User)
class UserAccountAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'phone', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'address')}),
        ('Contact info', {'fields': ('phone',)}),
        ('Permissions', {'classes': ('collapse',), 'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('Important dates', {'classes': ('collapse',), 'fields': ('last_login', 'date_joined')}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address', 'is_admin',
                       'is_staff', 'is_superuser'), }),)

    filter_horizontal = ()
    list_filter = ('is_staff', 'is_admin')
