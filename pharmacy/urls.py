from django.urls import path
from .views import (
    IndexView,
    about,
    contact,
    catalog,
    cart,
    GoodDetailView
)

# app_name = 'index'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('catalog/', catalog, name='catalog'),
    path('cart/', cart, name='cart'),
    path('good/<slug>/', GoodDetailView.as_view(), name='good')
]
