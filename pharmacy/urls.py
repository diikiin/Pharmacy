from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart')
]
