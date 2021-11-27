from django.urls import path
from .views import (
    IndexView,
    about,
    contact,
    catalog,
    cart,
    ItemDetailView,
    add_to_cart,
    remove_from_cart
)

# app_name = 'index'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('catalog/', catalog, name='catalog'),
    path('cart/', cart, name='cart'),
    path('good/<slug>/', ItemDetailView.as_view(), name='good'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')
]
