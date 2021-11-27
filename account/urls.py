from django.urls import path
from .views import (
    register,
    login,
    logout,
    profile,
    orders,
    password_change,
    password_reset
)

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('orders/', orders, name='orders'),
    path('password-change/', password_change, name='password change'),
    path('password-reset/', password_reset, name='password reset')
]
