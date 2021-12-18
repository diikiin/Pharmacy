from django.contrib import admin
from .models import Item, OrderItem, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'company', 'cost')
    search_fields = ('name', 'company')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')
    readonly_fields = ('pk', 'user', 'item', 'quantity', 'ordered')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered_date')
    readonly_fields = ('pk', 'user', 'items', 'address', 'phone', 'payment', 'ordered_date', 'ordered')
