from django.contrib import admin
from .models import Good, OrderGood, Order, Contact


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'company', 'cost')
    search_fields = ('name', 'company')


admin.site.register(OrderGood)
admin.site.register(Order)
