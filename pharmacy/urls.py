from django.urls import path
from .views import (
    index,
    about,
    contact,
    CatalogView,
    CartView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    checkout,
    CheckoutView
)

# app_name = 'index'

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('cart/', CartView.as_view(), name='cart'),
    path('item/<slug>/', ItemDetailView.as_view(), name='item'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout')
]
