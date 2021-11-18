from django.contrib import admin
from .models import Good, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message')
    search_fields = ('email', 'name')
    readonly_fields = ('name', 'phone', 'email', 'message')


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('img', 'name', 'description', 'company', 'cost')
    search_fields = ('name', 'company')


